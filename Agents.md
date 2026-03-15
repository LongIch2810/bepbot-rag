# RAG Project — Hướng dẫn dành cho Agent

## 1. Tổng quan dự án

Đây là một **chatbot RAG (Retrieval-Augmented Generation)** chuyên về **công thức nấu ăn Việt Nam**. Hệ thống đọc tài liệu PDF chứa 200 món ăn truyền thống, tách nhỏ văn bản, tạo embeddings, lưu vào vector database, và sử dụng LLM để trả lời câu hỏi của người dùng dựa trên nội dung tài liệu đã được lưu trữ.

**Ngôn ngữ**: Python  
**Framework chính**: LangChain  
**Chế độ chạy**: Console (CLI chatbot)

---

## 2. Tech Stack

| Thành phần          | Công nghệ                          | Ghi chú                                      |
| ------------------- | ----------------------------------- | --------------------------------------------- |
| **LLM**             | Google Gemini (`gemini-2.5-flash`)  | Qua `langchain-google-genai`                  |
| **Embeddings**      | Ollama (`nomic-embed-text-v2-moe`)  | Chạy local qua `langchain-ollama`             |
| **Vector Database** | Qdrant Cloud                        | Kết nối qua URL + API key trong `.env`        |
| **Document Loader** | `PyPDFLoader` (LangChain Community) | Load PDF từ thư mục `data/`                   |
| **Text Splitter**   | `RecursiveCharacterTextSplitter`    | chunk_size=900, chunk_overlap=180             |
| **Agent Framework** | `langchain.agents.create_agent`     | Agent có tool retriever để tìm kiếm ngữ cảnh |

---

## 3. Cấu trúc thư mục

```
rag-project/
├── .env                  # Biến môi trường (API keys, Qdrant URL)
├── .gitignore
├── requirements.txt      # Các thư viện Python cần cài đặt
├── data/
│   └── huong-dan-nau-an-200-mon-truyen-thong.pdf   # Tài liệu nguồn (51MB)
├── app/
│   ├── main.py           # Entry point — chạy chatbot CLI
│   ├── streamlit_app.py   # Entry point — giao diện web Streamlit
│   ├── workflow.py        # Orchestrator — khởi tạo & điều phối toàn bộ pipeline
│   ├── config.py          # Hằng số cấu hình (chunk size, model, collection name...)
│   ├── loader.py          # Load PDF documents từ thư mục data/
│   ├── splitter.py        # Tách documents thành chunks nhỏ
│   ├── embedder.py        # Tạo embedding model instance
│   ├── vectorstore.py     # Quản lý Qdrant collection & vector store
│   ├── retriever.py       # Tool tìm kiếm similarity trong vector store
│   ├── prompts.py         # Quản lý system prompt
│   ├── agent.py           # Wrapper tạo LangChain agent
│   └── rag.py             # File thử nghiệm (chứa code cũ/commented, không dùng trong pipeline chính)
└── venv/                  # Virtual environment (không commit)
```

---

## 4. Luồng hoạt động (Pipeline)

```
┌─────────────┐    ┌─────────────┐    ┌──────────────┐    ┌───────────────┐
│  Loader      │───▶│  Splitter    │───▶│  Embedder    │───▶│  VectorStore  │
│  (PDF → Doc) │    │  (Doc→Chunk) │    │  (→ vectors) │    │  (Qdrant)     │
└─────────────┘    └─────────────┘    └──────────────┘    └───────┬───────┘
                                                                  │
                                                                  ▼
┌─────────────┐    ┌─────────────┐    ┌──────────────┐    ┌───────────────┐
│  main.py     │───▶│  Workflow    │───▶│  Agent       │───▶│  Retriever    │
│  (User I/O)  │    │ (Orchestr.) │    │  (Gemini)    │    │  (sim_search) │
└─────────────┘    └─────────────┘    └──────────────┘    └───────────────┘
```

### Quá trình khởi tạo (chạy 1 lần):
1. `main.py` khởi tạo `Workflow`
2. `Workflow.__init__()` tạo tất cả các component: Loader, Splitter, Embedder, VectorStore, Retriever, Agent
3. `workflow.load_and_process_documents()` kiểm tra collection đã tồn tại trên Qdrant chưa:
   - **Chưa có** → Load PDF → Split → Tạo embeddings & lưu vào Qdrant
   - **Đã có** → Bỏ qua (tránh duplicate)

### Quá trình truy vấn (mỗi câu hỏi):
1. User nhập câu hỏi qua console
2. `workflow.retriever_and_generattion(query)` gọi Agent
3. Agent nhận câu hỏi, tự quyết định sử dụng **retrieve_context_tool** để tìm top-K (6) documents tương tự
4. Agent tổng hợp kết quả và trả lời bằng tiếng Việt

---

## 5. Chi tiết từng module

### `config.py`
Chứa tất cả hằng số cấu hình:
- `CHUNK_SIZE = 900` — Kích thước mỗi chunk (ký tự)
- `CHUNK_OVERLAP = 180` — Độ chồng lấn giữa các chunk
- `EMBEDDING_MODEL = "nomic-embed-text-v2-moe:latest"` — Model embedding chạy trên Ollama
- `LLM_MODEL = "gemini-2.5-flash"` — Model LLM
- `VECTOR_SIZE = 768` — Kích thước vector embedding
- `COLLECTION_NAME = "CONG_THUC_NAU_AN_COLLECTION"` — Tên collection trên Qdrant
- `TOP_K = 6` — Số lượng documents trả về khi search

### `loader.py` — Class `Loader`
- Đọc tất cả file `.pdf` trong thư mục `data/` (ngang cấp với `app/`)
- Sử dụng `PyPDFLoader` của LangChain
- Trả về list `Document` objects

### `splitter.py` — Class `Splitter`
- Sử dụng `RecursiveCharacterTextSplitter`
- Tách documents thành chunks nhỏ với `add_start_index=True` để theo dõi vị trí gốc

### `embedder.py` — Class `Embedder`
- Factory đơn giản tạo embedding model instance
- Nhận `embedding_class` (mặc định `OllamaEmbeddings`) và model name

### `vectorstore.py` — Class `VectorStore`
- Quản lý kết nối đến Qdrant Cloud qua `QdrantClient`
- `check_collection_exists()` — Kiểm tra collection có tồn tại không
- `create_collection()` — Tạo collection mới với Cosine distance
- `get_vector_store()` — Trả về `QdrantVectorStore` instance (tự tạo collection nếu chưa có)

### `retriever.py` — Class `Retriever`
- `retrieve_context(query)` — Thực hiện similarity search, trả về serialized text + raw docs
- `as_tool()` — Wrap thành LangChain `@tool` với `response_format="content_and_artifact"` để Agent có thể sử dụng

### `prompts.py` — Class `Prompts`
- Wrapper đơn giản cho system prompt string
- Prompt hiện tại yêu cầu Agent chỉ trả lời dựa trên tài liệu, không tự suy diễn

### `agent.py` — Class `Agent`
- Wrapper cho `langchain.agents.create_agent(model, tools, system_prompt=...)`
- Nhận LLM model, list tools, và system prompt

### `workflow.py` — Class `Workflow`
- **Orchestrator chính** của hệ thống
- Khởi tạo và kết nối tất cả các component
- `load_and_process_documents()` — Ingest documents (chỉ chạy lần đầu)
- `retriever_and_generattion(query)` — Xử lý truy vấn end-to-end

### `rag.py` — Class `RAG`
- File thử nghiệm ban đầu, phần lớn code đã bị comment out
- Class `RAG` còn lại là wrapper đơn giản cho agent invocation
- **Không được sử dụng** trong pipeline chính (main.py dùng `Workflow`)

### `main.py`
- Entry point CLI: `python main.py`
- Chạy vòng lặp input/output trên console
- Hỗ trợ thoát bằng `exit` hoặc `quit`

### `streamlit_app.py`
- Entry point web: `streamlit run app/streamlit_app.py`
- Giao diện chat trên trình duyệt (mặc định `localhost:8501`)
- Sử dụng `st.session_state` để lưu `Workflow` instance và lịch sử chat
- Hiển thị loading indicator trong quá trình khởi tạo và nạp tài liệu
- Chặn input cho đến khi `load_and_process_documents()` hoàn tất

---

## 6. Biến môi trường (`.env`)

| Biến               | Mô tả                        |
| ------------------- | ----------------------------- |
| `GOOGLE_API_KEY`    | API key cho Google Gemini     |
| `QDRANT_API_KEY`    | API key cho Qdrant Cloud      |
| `QDRANT_URL`        | URL endpoint của Qdrant Cloud |

---

## 7. Cách chạy dự án

```bash
# 1. Cài đặt dependencies
pip install -r requirements.txt

# 2. Đảm bảo Ollama đang chạy với model embedding
ollama pull nomic-embed-text-v2-moe

# 3. Cấu hình .env với các API keys

# 4a. Chạy chatbot CLI
cd app
python main.py

# 4b. Hoặc chạy giao diện web Streamlit
streamlit run app/streamlit_app.py
```

**Yêu cầu**:
- Python 3.10+
- Ollama phải đang chạy local (dùng cho embeddings)
- Kết nối internet (để gọi Google Gemini API và Qdrant Cloud)

---

## 8. Lưu ý quan trọng khi chỉnh sửa

1. **Imports sử dụng relative path** — Tất cả imports trong `app/` dùng tên module trực tiếp (vd: `from loader import Loader`), do đó phải chạy từ bên trong thư mục `app/`.
2. **File `rag.py` là code thử nghiệm** — Có thể xoá hoặc refactor mà không ảnh hưởng pipeline chính.
3. **Collection Qdrant chỉ tạo 1 lần** — Nếu đã có collection `CONG_THUC_NAU_AN_COLLECTION` trên Qdrant Cloud, hệ thống sẽ không re-index. Muốn re-index cần xoá collection thủ công.
4. **Typo trong code**: `retriever_and_generattion` (thừa chữ 't') — giữ nguyên khi refactor để không break.
5. **Embedding chạy local** — Model `nomic-embed-text-v2-moe` chạy qua Ollama, cần cài và pull model trước.
6. **Data folder** — Chứa file PDF ~51MB, không nên commit vào git.
