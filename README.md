# BepBot RAG

`BepBot RAG` là chatbot hỏi đáp về công thức nấu ăn Việt Nam, xây trên kiến trúc `Retrieval-Augmented Generation (RAG)`.
Hệ thống đọc tài liệu công thức, tạo embeddings, lưu vào Qdrant và dùng Gemini để trả lời bằng tiếng Việt dựa trên ngữ cảnh truy xuất được.

Phiên bản hiện tại có giao diện web Streamlit đã được cập nhật:

- Upload tài liệu người dùng (`PDF`, `DOCX`, `TXT`) để bổ sung nguồn tri thức.
- Gửi câu hỏi ngay trong khung chat.
- Mỗi lượt chat có thể đính kèm `1 ảnh`.
- Ảnh được phân tích bằng Gemini Vision để lấy `tên món ăn` và `text trong ảnh`, sau đó dùng làm ngữ cảnh bổ sung cho đúng lượt hỏi đó.

## Tính năng chính

- Hỏi đáp về món ăn Việt Nam dựa trên tài liệu hệ thống.
- Bổ sung tài liệu riêng của người dùng và truy vấn theo 3 chế độ:
  - `system_only`
  - `user_only`
  - `hybrid`
- Phân tích ảnh đính kèm theo từng tin nhắn:
  - nhận diện món ăn
  - đọc chữ trong ảnh
  - dùng nội dung ảnh để mở rộng truy vấn RAG
- Giao diện Streamlit thân thiện hơn cho nhập liệu và theo dõi hội thoại.

## Tech Stack

- LLM: `gemini-2.5-flash`
- Vision: `langchain-google-genai`
- Embeddings: `nomic-embed-text-v2-moe` qua `Ollama`
- Vector DB: `Qdrant Cloud`
- Framework: `LangChain`, `Streamlit`
- Ngôn ngữ: `Python 3.10+`

## Cấu trúc dự án

```text
rag-project/
├── app/
│   ├── config.py
│   ├── embedder.py
│   ├── image_text_extractor.py
│   ├── llm_scanning_content.py
│   ├── loader.py
│   ├── main.py
│   ├── prompts.py
│   ├── retriever.py
│   ├── splitter.py
│   ├── validator.py
│   ├── vectorstore.py
│   ├── vision_image.py
│   └── workflow.py
├── data/
├── utils/
├── streamlit_app.py
├── requirements.txt
└── .env
```

## Chuẩn bị môi trường

### 1. Tạo virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

macOS / Linux:

```bash
source venv/bin/activate
```

### 2. Cài dependencies

```bash
pip install -r requirements.txt
```

### 3. Chuẩn bị Ollama

Cài `Ollama` và tải model embedding:

```bash
ollama pull nomic-embed-text-v2-moe
```

Đảm bảo Ollama đang chạy khi khởi động app.

### 4. Cấu hình biến môi trường

Tạo file `.env` ở thư mục gốc:

```env
GOOGLE_API_KEY=your_google_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
```

### 5. Chuẩn bị dữ liệu

Đặt file PDF nguồn vào thư mục `data/`.

Ví dụ:

```text
data/huong-dan-nau-an-200-mon-truyen-thong.pdf
```

Ở lần chạy đầu tiên, hệ thống sẽ:

1. đọc tài liệu
2. chia chunk
3. tạo embeddings
4. đẩy dữ liệu lên Qdrant

Những lần sau, nếu collection đã tồn tại, hệ thống sẽ không re-index lại.

## Chạy ứng dụng

### Giao diện web Streamlit

Đây là entrypoint chính hiện tại:

```bash
streamlit run streamlit_app.py
```

Ứng dụng mặc định chạy tại:

```text
http://localhost:8501
```

### Giao diện CLI

CLI vẫn có sẵn để test nhanh:

```bash
python -m app.main
```

## Cách dùng giao diện web

### 1. Upload tài liệu

Trong sidebar:

- tải lên `PDF`, `DOCX`, hoặc `TXT`
- bấm `Xử lý tài liệu`
- hệ thống kiểm duyệt nội dung rồi nạp vào user knowledge base

### 2. Chọn chế độ trả lời

- `Chỉ dùng tài liệu hệ thống`
- `Chỉ dùng tài liệu người dùng`
- `Dùng cả hai nguồn`

### 3. Chat kèm ảnh

Trong khung chat:

- nhập câu hỏi
- có thể đính kèm `1 ảnh JPG/PNG/JPEG` cho đúng lượt hỏi đó

Ảnh sẽ được:

- hiển thị ngay trong bubble của người dùng
- phân tích bằng Gemini Vision
- trích `nhãn ảnh / tên món`
- trích `text_content` nếu ảnh có chữ
- dùng làm ngữ cảnh phụ cho câu trả lời của lượt chat đó

### 4. Nhận câu trả lời

Hệ thống sẽ kết hợp:

- ngữ cảnh truy xuất từ Qdrant
- chế độ truy vấn đang chọn
- thông tin trích từ ảnh đính kèm

## Luồng xử lý

### Ingestion

```text
PDF/TXT/DOCX
-> Loader
-> Splitter
-> Embeddings
-> Qdrant
```

### Query

```text
User question
-> optional image analysis
-> retrieval query expansion
-> Retriever
-> Gemini answer generation
```

## Các file quan trọng

- [streamlit_app.py](streamlit_app.py): giao diện web chính
- [app/workflow.py](app/workflow.py): điều phối toàn bộ luồng RAG
- [app/validator.py](app/validator.py): kiểm duyệt file upload và ảnh
- [app/image_text_extractor.py](app/image_text_extractor.py): wrapper Vision để đọc thông tin từ ảnh
- [app/vision_image.py](app/vision_image.py): structured output cho phân tích ảnh
- [app/retriever.py](app/retriever.py): truy xuất ngữ cảnh từ vector store

## Lưu ý

- `rag.py` là file thử nghiệm cũ, không thuộc pipeline chính.
- Dự án hiện ưu tiên luồng Streamlit hơn CLI.
- Mỗi lần chat chỉ nên đính kèm tối đa `1 ảnh`.
- Ảnh không được lưu vào vector store; chỉ dùng làm ngữ cảnh cho lượt hỏi hiện tại.

## Lệnh hữu ích

Chạy kiểm tra syntax nhanh:

```bash
python -m py_compile streamlit_app.py app/workflow.py app/validator.py
```
