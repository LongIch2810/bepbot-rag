import os
import tempfile
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from docx2pdf import convert


def get_docs_user_upload_files(uploaded_file):
    temp_path = None

    try:
        temp_path = get_temp_path(uploaded_file)
        ext = Path(uploaded_file.name).suffix.lower()

        if ext == ".pdf":
            docs = PyPDFLoader(temp_path).load()
        elif ext == ".docx":
            docs = Docx2txtLoader(temp_path).load()
        elif ext == ".txt":
            try:
                docs = TextLoader(temp_path, encoding="utf-8").load()
            except UnicodeDecodeError:
                docs = TextLoader(temp_path, encoding="latin-1").load()
        else:
            raise ValueError("Chỉ hỗ trợ file PDF, DOCX, TXT")

        for index, doc in enumerate(docs):
            old_metadata = doc.metadata or {}
            doc.metadata = {
                **old_metadata,
                "source_type": "user",
                "file_name": uploaded_file.name,
                "page": old_metadata.get("page", index + 1),
            }

        return docs

    except Exception as e:
        print(f"Lỗi khi đọc file '{uploaded_file.name}': {e}")
        return []

    finally:
        # Xóa file tạm sau khi xử lý xong
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


def get_temp_path(uploaded_file):
    suffix = Path(uploaded_file.name).suffix.lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        return tmp_file.name


def convert_docx_to_pdf_bytes(uploaded_file):
    with tempfile.TemporaryDirectory() as temp_dir:
        docx_path = Path(temp_dir) / uploaded_file.name
        pdf_path = docx_path.with_suffix(".pdf")

        docx_path.write_bytes(uploaded_file.getvalue())
        convert(str(docx_path), str(pdf_path))

        return pdf_path.read_bytes()
