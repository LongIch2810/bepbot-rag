from app.config import TOP_K, SYSTEM_ONLY, USER_ONLY, HYBRID


class Retriever:
    def __init__(self, vector_store, user_vector_store):
        self.vector_store = vector_store
        self.user_vector_store = user_vector_store

    def retrieve_context(self, query: str, mode: str = SYSTEM_ONLY):
        if mode == SYSTEM_ONLY:
            retrieved_docs = self.vector_store.get_vector_store().similarity_search(
                query, k=TOP_K
            )
        elif mode == USER_ONLY:
            if self.user_vector_store is None:
                raise ValueError("User vector store is not ready.")
            retrieved_docs = self.user_vector_store.similarity_search(query, k=TOP_K)
        elif mode == HYBRID:
            if self.user_vector_store is None:
                raise ValueError("User vector store is not ready.")

            system_docs = self.vector_store.get_vector_store().similarity_search(
                query, k=TOP_K
            )
            user_docs = self.user_vector_store.similarity_search(query, k=TOP_K)

            serialized_system = "\n\n".join(
                f"[HỆ THỐNG]\nSource: {doc.metadata}\nContent: {doc.page_content}"
                for doc in system_docs
            )
            serialized_user = "\n\n".join(
                f"[NGƯỜI DÙNG]\nSource: {doc.metadata}\nContent: {doc.page_content}"
                for doc in user_docs
            )

            serialized = f"""
=== NGỮ CẢNH TỪ TÀI LIỆU HỆ THỐNG ===
{serialized_system}

=== NGỮ CẢNH TỪ TÀI LIỆU NGƯỜI DÙNG ===
{serialized_user}
""".strip()

            retrieved_docs = {
                "system_docs": system_docs,
                "user_docs": user_docs,
            }
            return serialized, retrieved_docs
        else:
            raise ValueError(f"Unsupported mode: {mode}")
        serialized = "\n\n".join(
            (f"Source: {doc.metadata}\nContent: {doc.page_content}")
            for doc in retrieved_docs
        )
        return serialized, retrieved_docs

    def set_user_vector_store(self, user_vector_store):
        self.user_vector_store = user_vector_store
