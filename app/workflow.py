import os
from loader import Loader
from splitter import Splitter
from embedder import Embedder
from vectorstore import VectorStore
from retriever import Retriever
from prompts import Prompts
from agent import Agent
from config import CHUNK_SIZE,CHUNK_OVERLAP,EMBEDDING_MODEL,VECTOR_SIZE, COLLECTION_NAME,TOP_K,LLM_MODEL
from langchain_ollama import OllamaEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
class Workflow:
    def __init__(self):
        self.loader = Loader()
        self.splitter = Splitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
        self.embedder = Embedder(embedding_model=EMBEDDING_MODEL)
        embeddings = self.embedder.get_embbeddings(OllamaEmbeddings)
        self.vector_store = VectorStore(qdrant_url=os.getenv("QDRANT_URL"),
                           qdrant_api_key=os.getenv("QDRANT_API_KEY"),
                           collection_name=COLLECTION_NAME,
                           vector_size=VECTOR_SIZE,embeddings=embeddings)
        self.retriever = Retriever(self.vector_store)
        model = ChatGoogleGenerativeAI(model=LLM_MODEL,
                               google_api_key=os.getenv("GOOGLE_API_KEY"),
                               temperature=0.3)
        tools = [self.retriever.as_tool()]
        self.prompt = Prompts(
            (
            "Bạn có quyền truy cập vào một công cụ dùng để truy xuất ngữ cảnh từ các tài liệu hướng dẫn nấu ăn bằng tiếng Việt. "
            "Hãy sử dụng công cụ đó để trả lời các câu hỏi của người dùng về hướng dẫn nấu ăn, nguyên liệu, "
            "cách nêm nếm, các bước thực hiện món ăn, kỹ thuật nấu, mẹo nấu ăn, và hướng dẫn thực hiện công thức món ăn Việt Nam. "
            "Chỉ được trả lời dựa trên thông tin được nêu rõ trong tài liệu đã cung cấp. "
            "Không tự suy diễn, không giả định, và không tự bịa thêm thông tin không có trong tài liệu."
            )
        )
        self.agent = Agent(model,tools,self.prompt.get_system_prompt())
        
    def load_and_process_documents(self):
        print(self.vector_store.check_collection_exists())
        if not self.vector_store.check_collection_exists():
            docs = self.loader.load_documents()
            all_splits = self.splitter.split_docs(docs)
            self.vector_store.get_vector_store().add_documents(documents=all_splits)
            
    def retriever_and_generattion(self, query):
        result = self.agent.get_agent().invoke(
            {"messages": [{"role": "user", "content": query}]}
        )
        return result["messages"][-1].content[0]["text"]