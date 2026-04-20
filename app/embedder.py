from langchain_ollama import OllamaEmbeddings


class Embedder:
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model

    def get_embbeddings(self, embeddings_class):
        embeddings = embeddings_class(model=self.embedding_model)
        return embeddings
