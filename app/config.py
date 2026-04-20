CHUNK_SIZE = 900
CHUNK_OVERLAP = 180
EMBEDDING_MODEL = "nomic-embed-text-v2-moe:latest"
LLM_MODEL = "gemini-2.5-flash"
VECTOR_SIZE = 768
COLLECTION_NAME = "CONG_THUC_NAU_AN_COLLECTION"
TOP_K = 6
MAX_UPLOAD_FILES = 3
MAX_UPLOAD_FILE_MB = 50
MAX_UPLOAD_IMAGE_MB = 10
MAX_UPLOAD_IMAGES = 1
SYSTEM_ONLY = "system_only"
USER_ONLY = "user_only"
HYBRID = "hybrid"
FILE_ACCEPT = [
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
]
IMAGE_ACCEPT = ["image/jpeg", "image/png", "image/jpg"]
