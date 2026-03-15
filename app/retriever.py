from langchain.tools import tool
from config import TOP_K
class Retriever:
    def __init__(self,vector_store):
        self.vector_store = vector_store
        
    def retrieve_context(self, query: str):
        retrieved_docs = self.vector_store.get_vector_store().similarity_search(query, k=TOP_K)
        serialized = "\n\n".join(
                (f"Source: {doc.metadata}\nContent: {doc.page_content}")
                    for doc in retrieved_docs
        )
        return serialized,retrieved_docs
    
    def as_tool(self):
        @tool(response_format="content_and_artifact")
        def retrieve_context_tool(query:str):
            """Retrieve information to help answer a query."""
            return self.retrieve_context(query)
        return retrieve_context_tool
            