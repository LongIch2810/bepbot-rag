import base64

from langchain_core.messages import HumanMessage, SystemMessage

from app.vision_image import structured_llm


class ImageTextExtractor:
    def __init__(self):
        pass

    def _build_messages(self, upload_file):
        image_bytes = upload_file.getvalue()
        image_data = base64.b64encode(image_bytes).decode("utf-8")
        mime_type = upload_file.type or "image/jpeg"

        return [
            SystemMessage(
                content="""
Bạn là bộ phân tích hình ảnh cho hệ thống RAG về ẩm thực.

Nhiệm vụ:
- Xác định ảnh có phải ảnh món ăn hay không.
- Đặt nhãn ngắn gọn cho chủ thể chính trong ảnh.
- Xác định ảnh có chứa chữ hay không.
- Nếu có chữ, trích xuất đầy đủ phần chữ nhìn thấy được trong ảnh vào trường `text_content`.
- Chỉ dựa trên nội dung nhìn thấy trong ảnh.
- Không bịa thêm thông tin.
- Luôn trả kết quả đúng schema.
                """.strip()
            ),
            HumanMessage(
                content=[
                    {
                        "type": "text",
                        "text": (
                            "Hãy phân tích ảnh này và trả kết quả theo schema. "
                            "Nếu ảnh có chữ, ưu tiên đọc và trích xuất chính xác phần chữ."
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{image_data}",
                        },
                    },
                ]
            ),
        ]

    def analyze(self, upload_file):
        messages = self._build_messages(upload_file)
        return structured_llm.invoke(messages)

    def extract_text(self, upload_file):
        result = self.analyze(upload_file)
        return result.text_content.strip() if result.text_content else ""

    def excute(self, upload_file):
        return self.extract_text(upload_file)
