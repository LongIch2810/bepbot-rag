from langchain_text_splitters import RecursiveCharacterTextSplitter
class Splitter:
    def __init__ (self, chunk_size, chunk_overlap):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
    def split_docs(self, docs):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,  # chunk size (characters)
            chunk_overlap=self.chunk_overlap,  # chunk overlap (characters)
            add_start_index=True,  # track index in original document
            
        )
        all_splits = text_splitter.split_documents(docs)
        return all_splits