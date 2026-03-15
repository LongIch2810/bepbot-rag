# 🍲 BếpBot RAG - Vietnamese Recipe Assistant

**BếpBot RAG** là một hệ thống chatbot thông minh ứng dụng kiến trúc **Retrieval-Augmented Generation (RAG)**, chuyên giải đáp và hướng dẫn nấu 200 món ăn truyền thống của Việt Nam. Hệ thống thực hiện trích xuất dữ liệu từ tài liệu tham khảo chuẩn, số hóa bằng mô hình nhúng (Embeddings) và sử dụng LLM để cung cấp câu trả lời chính xác, sát với nguyên bản nhất.

Dự án cá nhân này được thiết kế để trình diễn luồng xây dựng một ứng dụng RAG hoàn chỉnh kết hợp giữa các dịch vụ Cloud và Local AI.

---

## 🚀 Tính năng nổi bật

- **Hỏi đáp thông minh**: Trả lời chính xác công thức, nguyên liệu, và tỷ lệ cách làm dựa trên tài liệu gốc, không tự bịa thông tin.
- **Nguồn dữ liệu chuẩn**: Tích hợp sách hướng dẫn 200 món ăn truyền thống gia đình.
- **Đa nền tảng giao diện**: Hỗ trợ cả giao diện dòng lệnh (CLI) tốc độ cao và giao diện Web trực quan (Streamlit).
- **Tối ưu chi phí & Bảo mật**: Sử dụng Local Embeddings chạy trên máy cá nhân để vectorize tài liệu.

## 🛠 Tech Stack

- **Large Language Model (LLM)**: Google Gemini (`gemini-2.5-flash`) thông qua `langchain-google-genai`.
- **Embeddings**: Ollama (`nomic-embed-text-v2-moe`) chạy Local.
- **Vector Database**: Qdrant Cloud.
- **Framework**: LangChain, Streamlit.
- **Ngôn ngữ**: Python 3.10+

## 📂 Cấu trúc dự án

```text
bepbot-rag/
├── app/
│   ├── main.py            # Entry point: Chạy chatbot giao diện CLI
│   ├── streamlit_app.py   # Entry point: Chạy giao diện Web (Streamlit)
│   ├── workflow.py        # Orchestrator: Điều phối toàn bộ pipeline RAG
│   ├── config.py          # Quản lý hằng số và cấu hình hệ thống
│   ├── loader.py          # Module đọc file PDF (PyPDFLoader)
│   ├── splitter.py        # Module chia nhỏ văn bản (RecursiveCharacterTextSplitter)
│   ├── embedder.py        # Module tạo mô hình Embeddings
│   ├── vectorstore.py     # Module kết nối và quản lý Qdrant Collection
│   ├── retriever.py       # Công cụ tìm kiếm vector (Similarity Search)
│   ├── prompts.py         # Quản lý System Prompt cho Agent
│   └── agent.py           # Thiết lập LangChain Agent với công cụ truy xuất
├── data/
│   └── huong-dan-nau-an-200-mon-truyen-thong.pdf  # Tài liệu nguồn định dạng PDF
├── .env.example           # File mẫu tham khảo các biến môi trường
├── .gitignore
└── requirements.txt       # Danh sách các thư viện phụ thuộc
```

## ⚙️ Hướng dẫn cài đặt

### 1. Chuẩn bị môi trường & Cài đặt thư viện

```bash
# Clone repository
git clone https://github.com/LongIch2810/bepbot-rag.git
cd bepbot-rag

# Khởi tạo và kích hoạt virtual environment (Khuyến nghị)
python -m venv venv
# Trên Windows:
venv\Scripts\activate
# Trên macOS/Linux:
source venv/bin/activate

# Cài đặt các thư viện yêu cầu
pip install -r requirements.txt
```

### 2. Thiết lập Ollama (Local Embeddings)

Dự án sử dụng mô hình embedding chạy local qua Ollama để tối ưu hiệu suất và chi phí.

- Cài đặt [Ollama](https://ollama.com/) vào máy tính của bạn.
- Tải mô hình embedding được chỉ định (Model này cực nhẹ và tối ưu cho CPU):
  ```bash
  ollama pull nomic-embed-text-v2-moe
  ```
- Đảm bảo ứng dụng Ollama đang được chạy nền.

### 3. Cấu hình biến môi trường

Tạo file `.env` ở thư mục gốc của dự án (hoặc đổi tên file `.env.example` thành `.env`) và điền các API Key của bạn:

```env
GOOGLE_API_KEY=your_gemini_api_key
QDRANT_URL=your_qdrant_cloud_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
```

### 4. Chuẩn bị dữ liệu

> **Lưu ý quan trọng**: Do file tài liệu gốc (`huong-dan-nau-an-200-mon-truyen-thong.pdf`) có dung lượng khá lớn (~51MB), file này **KHÔNG** được tải lên thư mục Github để giữ repo nhẹ nhất có thể.

Để hệ thống hoạt động, bạn cần:

1. Tạo thư mục `data/` ở thư mục gốc của dự án (nếu chưa có).
2. Tải file tài liệu PDF gốc (bạn có thể cung cấp link Google Drive/Dropbox tải file ở đây) hoặc dùng bất kỳ file PDF nào bạn muốn chatbot đọc.
3. Đặt file đó vào trong thư mục `data/`. Loader của hệ thống sẽ tự động quét và nhúng dữ liệu vào lần chạy đầu tiên.

## ▶️ Hướng dẫn sử dụng

Hệ thống được thiết kế tự động hoàn toàn: ở lần khởi chạy đầu tiên, mã nguồn sẽ đọc PDF, chunking tài liệu, vectorize và đẩy lên Qdrant Collection. Ở các lần chạy sau, hệ thống sẽ bỏ qua bước này để tối ưu thời gian khởi động.

**Cách 1: Chạy giao diện Console (CLI)**
Dành cho người thích sự nhanh gọn, thao tác qua Terminal:

```bash
cd app
python main.py
```

> _(Gõ `exit` hoặc `quit` để thoát)_

**Cách 2: Chạy giao diện Web (Streamlit)**
Trải nghiệm không gian chat UI trực quan cực mượt trên trình duyệt:

```bash
streamlit run app/streamlit_app.py
```

> _(Mặc định truy cập tại `http://localhost:8501`)_

## 📝 Luồng xử lý kỹ thuật (Pipeline RAG)

1. **Data Ingestion**: Quét thư mục `data/` -> Phân tích PDF -> Tách nhỏ đoạn văn (Chunk size: 900 / Overlap: 180).
2. **Vectorization**: Mã hóa các phân đoạn nội dung thành Vector nhúng (768 dimensions) bằng Ollama.
3. **Storage**: Lưu trữ Vectors vào giao diện Qdrant Cloud.
4. **Retrieval & Generation**: Từ Command người dùng -> Agent sử dụng Tool tìm kiếm Top 6 node kết quả gần giống nhất bằng Cosine Distance -> LLM phân tích ngữ cảnh và sinh ngôn ngữ tự nhiên tiếng Việt trả về user.

---

_Được phát triển với niềm đam mê chia sẻ và gìn giữ văn hóa ẩm thực truyền thống Việt Nam._ 🇻🇳❤️
