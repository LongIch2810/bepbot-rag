import os
from loader import Loader
from splitter import Splitter
from embedder import Embedder
from vectorstore import VectorStore
from config import CHUNK_SIZE,CHUNK_OVERLAP,EMBEDDING_MODEL,VECTOR_SIZE, COLLECTION_NAME,TOP_K,LLM_MODEL
from langchain_ollama import OllamaEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
loader = Loader()
docs = loader.load_documents()
print("Documents loaded : ",len(docs))
splitter = Splitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
all_splits = splitter.split_docs(docs)
print(len(all_splits),type(all_splits))
embedder = Embedder(embedding_model=EMBEDDING_MODEL)
embeddings = embedder.get_embbeddings(OllamaEmbeddings)
vector_store = VectorStore(qdrant_url=os.getenv("QDRANT_URL"),
                           qdrant_api_key=os.getenv("QDRANT_API_KEY"),
                           collection_name=COLLECTION_NAME,
                           vector_size=VECTOR_SIZE,embeddings=embeddings)
# document_ids =vector_store.get_vector_store().add_documents(documents=all_splits)
# print(len(document_ids))
# from langchain.tools import tool

# @tool(response_format="content_and_artifact")
# def retrieve_context(query: str):
#     """Retrieve information to help answer a query."""
#     retrieved_docs = vector_store.get_vector_store().similarity_search(query, k=TOP_K)
#     serialized = "\n\n".join(
#                (f"Source: {doc.metadata}\nContent: {doc.page_content}")
#                 for doc in retrieved_docs
#     )
#     return serialized,retrieved_docs

# from langchain.agents import create_agent
# model = ChatGoogleGenerativeAI(model=LLM_MODEL,
#                                google_api_key=os.getenv("GOOGLE_API_KEY"),
#                                temperature=0.3)
# tools = [retrieve_context]

# prompt = (
#     "Bạn có quyền truy cập vào một công cụ dùng để truy xuất ngữ cảnh từ các tài liệu hướng dẫn nấu ăn bằng tiếng Việt. "
#     "Hãy sử dụng công cụ đó để trả lời các câu hỏi của người dùng về hướng dẫn nấu ăn, nguyên liệu, "
#     "cách nêm nếm, các bước thực hiện món ăn, kỹ thuật nấu, mẹo nấu ăn, và hướng dẫn thực hiện công thức món ăn Việt Nam. "
#     "Chỉ được trả lời dựa trên thông tin được nêu rõ trong tài liệu đã cung cấp. "
#     "Không tự suy diễn, không giả định, và không tự bịa thêm thông tin không có trong tài liệu."
# )

# agent = create_agent(model, tools, system_prompt=prompt)

# query = "liệt kê các loại cà dùng để muối chua ?"

# result = agent.invoke(
#     {"messages": [{"role": "user", "content": query}]}
# )

# print(result["messages"][-1].content[0]["text"])
    
class RAG:
    def __init__(self,agent):
        self.agent = agent
        
        
    def _execute(self, query):
        result = self.agent.invoke(
            {"messages": [{"role": "user", "content": query}]}
        )
        return result["messages"][-1].content[0]["text"]