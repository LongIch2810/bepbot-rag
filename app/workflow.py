import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import OllamaEmbeddings

from app.config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    LLM_MODEL,
    VECTOR_SIZE,
)
from app.embedder import Embedder
from app.loader import Loader
from app.prompts import Prompts
from app.retriever import Retriever
from app.splitter import Splitter
from app.validator import Validator
from app.vectorstore import VectorStore

load_dotenv()


class Workflow:
    def __init__(self):
        self.loader = Loader()
        self.splitter = Splitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
        self.embedder = Embedder(embedding_model=EMBEDDING_MODEL)
        self.embeddings = self.embedder.get_embbeddings(OllamaEmbeddings)
        self.vector_store = VectorStore(
            qdrant_url=os.getenv("QDRANT_URL"),
            qdrant_api_key=os.getenv("QDRANT_API_KEY"),
            collection_name=COLLECTION_NAME,
            vector_size=VECTOR_SIZE,
            embeddings=self.embeddings,
        )
        self.validator = Validator()
        self.user_vector_store = None
        self.retriever = Retriever(self.vector_store, self.user_vector_store)
        self.model = ChatGoogleGenerativeAI(
            model=LLM_MODEL,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.3,
        )
        self.prompt = Prompts(
            (
                "Bạn là trợ lý RAG và phải trả lời bằng tiếng Việt. "
                "Bạn chỉ được dựa trên các nguồn được cung cấp trong prompt. "
                "Nguồn có thể gồm: tài liệu hệ thống, tài liệu người dùng, và thông tin trích từ ảnh người dùng upload. "
                "Khi trả lời, phải nêu rõ thông tin nào đến từ tài liệu hệ thống, thông tin nào đến từ tài liệu người dùng, "
                "và thông tin nào đến từ ảnh. "
                "Không tự suy diễn, không giả định, không bịa thêm thông tin ngoài các nguồn đã cung cấp."
            )
        )

    def load_and_process_documents(self):
        if not self.vector_store.check_collection_exists():
            docs = self.loader.load_system_documents()
            all_splits = self.splitter.split_docs(docs)
            self.vector_store.get_vector_store().add_documents(documents=all_splits)

    def build_user_vector_store(self, upload_files):
        docs = self.loader.load_uploaded_documents(upload_files)
        all_splits = self.splitter.split_docs(docs)
        self.user_vector_store = InMemoryVectorStore(embedding=self.embeddings)
        self.user_vector_store.add_documents(documents=all_splits)

    def prepare_user_uploads(self, upload_files):
        if not upload_files:
            raise ValueError("No upload files provided.")
        self.build_user_vector_store(upload_files)
        self.retriever.set_user_vector_store(self.user_vector_store)

    def _build_image_context(self, image_analysis_results):
        if not image_analysis_results:
            return ""

        image_contexts = []
        for result in image_analysis_results:
            if result.get("error"):
                continue

            parts = [f"Tên file ảnh: {result['file_name']}"]

            if result.get("image_label"):
                parts.append(
                    f"Nhãn/chủ đề chính trong ảnh: {result['image_label']}"
                )

            parts.append(
                "Ảnh món ăn: "
                + (
                    "có"
                    if result.get("is_food_image")
                    else "không rõ hoặc không phải"
                )
            )
            parts.append("Ảnh có chữ: " + ("có" if result.get("is_text") else "không"))

            if result.get("text_content"):
                parts.append(f"Nội dung chữ trích từ ảnh: {result['text_content']}")

            image_contexts.append("\n".join(parts))

        return "\n\n".join(image_contexts)

    def _build_retrieval_query(self, query, image_context):
        if not image_context:
            return query

        return f"{query}\n\nThông tin trích từ ảnh:\n{image_context}"

    def retriever_and_generattion(self, query, mode, image_analysis_results=None):
        if not query.strip():
            raise ValueError("Query is empty.")

        image_context = self._build_image_context(image_analysis_results or [])
        retrieval_query = self._build_retrieval_query(query, image_context)
        context, docs = self.retriever.retrieve_context(retrieval_query, mode)

        messages = [
            SystemMessage(content=self.prompt.get_system_prompt()),
            HumanMessage(
                content=f"""
Chế độ truy xuất: {mode}

Ngữ cảnh tài liệu:
{context}

Thông tin trích từ ảnh người dùng:
{image_context or "Không có"}

Câu hỏi của người dùng:
{query}
""".strip()
            ),
        ]

        response = self.model.invoke(messages)
        return response.content
