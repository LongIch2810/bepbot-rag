from app.config import MAX_UPLOAD_IMAGE_MB
from app.config import MAX_UPLOAD_IMAGES
from app.config import IMAGE_ACCEPT
from app.config import SYSTEM_ONLY, USER_ONLY, HYBRID
from app.llm_scanning_content import structured_llm
from app.image_text_extractor import ImageTextExtractor
from utils.utils import convert_docx_to_pdf_bytes
from app.config import MAX_UPLOAD_FILES, MAX_UPLOAD_FILE_MB, FILE_ACCEPT
from langchain_core.messages import HumanMessage, SystemMessage
import base64
from pathlib import Path


class Validator:
    def __init__(self):
        self.image_text_extractor = ImageTextExtractor()

    def calculate_total_size(self, uploaded_files):
        total_size = sum(file.size for file in uploaded_files)
        return total_size

    def validate_file_extension(self, uploaded_files):
        for uploaded_file in uploaded_files:
            if uploaded_file.type not in FILE_ACCEPT:
                return False, f"File {uploaded_file.name} is not supported"
        return True, "File extension is valid"

    def validate_mode(self, mode):
        if mode not in [SYSTEM_ONLY, USER_ONLY, HYBRID]:
            return False, "Invalid mode"
        return True, "Mode is valid"

    def validate_image_extension(self, upload_file):
        if upload_file.type not in IMAGE_ACCEPT:
            return False, f"File {upload_file.name} is not supported"
        return True, "Image is valid"

    def analyze_uploaded_images(self, uploaded_images):
        results = []

        for upload_file in uploaded_images:
            try:
                analysis = self.image_text_extractor.analyze(upload_file)
                results.append(
                    {
                        "file_name": upload_file.name,
                        "is_food_image": analysis.is_food_image,
                        "image_label": analysis.image_label,
                        "is_text": analysis.is_text,
                        "text_content": analysis.text_content.strip()
                        if analysis.text_content
                        else "",
                    }
                )
            except Exception as exc:
                results.append(
                    {
                        "file_name": upload_file.name,
                        "is_food_image": False,
                        "image_label": "",
                        "is_text": False,
                        "text_content": "",
                        "error": str(exc),
                    }
                )

        return results

    def validate_image_content(self, upload_file):
        result = None
        try:
            image_bytes = upload_file.getvalue()
            image_data = base64.b64encode(image_bytes).decode("utf-8")
            messages = [
                SystemMessage(
                    content="""
Bạn là bộ kiểm duyệt file upload cho hệ thống RAG về ẩm thực.

Nhiệm vụ:
- Xác định file có liên quan đến ẩm thực, món ăn, công thức nấu ăn, nguyên liệu, cách chế biến hay không.
- Chỉ dựa trên nội dung tài liệu được cung cấp.
- Không bịa thêm thông tin.
- Trường content phải ngắn gọn.
- Luôn trả kết quả đúng schema.
                    """.strip()
                ),
                HumanMessage(
                    content=[
                        {
                            "type": "text",
                            "text": "Hãy phân tích file này và trả kết quả theo schema.",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            },
                        },
                    ]
                ),
            ]
        except Exception as e:
            result = {
                "is_food_related": False,
                "content": str(e),
            }
        result = structured_llm.invoke(messages)
        return result

    def validate_food_content(self, upload_files):
        results = []
        for file in upload_files:
            try:
                ext = Path(file.name).suffix.lower()
                file_bytes = file.getvalue()

                if ext == ".pdf":
                    file_base64 = base64.b64encode(file_bytes).decode("utf-8")
                    mime_type = "application/pdf"
                    content_block = {
                        "type": "file",
                        "source_type": "base64",
                        "mime_type": mime_type,
                        "data": file_base64,
                    }
                elif ext == ".docx":
                    pdf_bytes = convert_docx_to_pdf_bytes(file)
                    file_base64 = base64.b64encode(pdf_bytes).decode("utf-8")
                    mime_type = "application/pdf"
                    content_block = {
                        "type": "file",
                        "source_type": "base64",
                        "mime_type": mime_type,
                        "data": file_base64,
                    }
                elif ext == ".txt":
                    # Decode as plain text and send as a text block directly
                    text_content = file_bytes.decode("utf-8", errors="replace")
                    content_block = {
                        "type": "text",
                        "text": f"Nội dung file:\n\n{text_content}",
                    }
                else:
                    results.append(
                        {
                            "file_name": file.name,
                            "is_food_related": False,
                            "content": f"Unsupported file type: {ext}",
                        }
                    )
                    continue

                messages = [
                    SystemMessage(
                        content="""
Bạn là bộ kiểm duyệt file upload cho hệ thống RAG về ẩm thực.

Nhiệm vụ:
- Xác định file có liên quan đến ẩm thực, món ăn, công thức nấu ăn, nguyên liệu, cách chế biến hay không.
- Chỉ dựa trên nội dung tài liệu được cung cấp.
- Không bịa thêm thông tin.
- Trường content phải ngắn gọn.
- Luôn trả kết quả đúng schema.
                    """.strip()
                    ),
                    HumanMessage(
                        content=[
                            {
                                "type": "text",
                                "text": "Hãy phân tích file này và trả kết quả theo schema.",
                            },
                            content_block,
                        ]
                    ),
                ]

                result = structured_llm.invoke(messages)
                results.append(
                    {
                        "file_name": file.name,
                        "is_food_related": result.is_food_related,
                        "content": result.content,
                    }
                )

            except Exception as e:
                results.append(
                    {
                        "file_name": file.name,
                        "is_food_related": False,
                        "content": str(e),
                    }
                )

        return results

    def validate_upload_images(self, uploaded_images):
        if not uploaded_images:
            return False, "No images uploaded"
        for uploaded_image in uploaded_images:
            is_valid, message = self.validate_image_extension(uploaded_image)
            if not is_valid:
                return False, message
        if len(uploaded_images) > MAX_UPLOAD_IMAGES:
            return False, f"You can only upload {MAX_UPLOAD_IMAGES} images"
        if (
            self.calculate_total_size(uploaded_images)
            > MAX_UPLOAD_IMAGE_MB * 1024 * 1024
        ):
            return (
                False,
                f"Total size of images exceeds the limit of {MAX_UPLOAD_IMAGE_MB} MB",
            )
        return True, "Upload images successfully"

    def validate_upload_files(self, uploaded_files):
        is_valid, message = self.validate_file_extension(uploaded_files)
        if not is_valid:
            return False, message
        if len(uploaded_files) > MAX_UPLOAD_FILES:
            return False, f"You can only upload {MAX_UPLOAD_FILES} files"
        if self.calculate_total_size(uploaded_files) > MAX_UPLOAD_FILE_MB * 1024 * 1024:
            return (
                False,
                f"Total size of files exceeds the limit of {MAX_UPLOAD_FILE_MB} MB",
            )
        return True, "Upload files successfully"
