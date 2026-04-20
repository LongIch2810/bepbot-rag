from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient


class VectorStore:
    def __init__(
        self, qdrant_url, qdrant_api_key, collection_name, vector_size, embeddings
    ):
        self.qdrant_url = qdrant_url
        self.qdrant_api_key = qdrant_api_key
        self.collection_name = collection_name
        self.vector_size = vector_size
        self.embeddings = embeddings
        self.client = QdrantClient(
            url=self.qdrant_url,
            api_key=self.qdrant_api_key,
        )

    def check_collection_exists(self):
        return self.client.collection_exists(self.collection_name)

    def create_collection(self):
        if not self.check_collection_exists():
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size, distance=Distance.COSINE
                ),
            )

    def get_vector_store(self):
        self.create_collection()
        vector_store = QdrantVectorStore(
            client=self.client,
            collection_name=self.collection_name,
            embedding=self.embeddings,
        )

        return vector_store
