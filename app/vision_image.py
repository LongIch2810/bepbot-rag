import os
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import LLM_MODEL
from dotenv import load_dotenv

load_dotenv()


class ImageVisionResult(BaseModel):
    is_food_image: bool = Field(
        description="True nếu là ảnh món ăn, False nếu không phải"
    )
    image_label: str = Field(
        description=(
            "Tên hoặc nhãn mô tả ngắn gọn của đối tượng/chủ thể chính trong ảnh. "
            "Ví dụ: 'Thịt kho trứng', 'Bún bò Huế', 'Tháp Eiffel', 'Chùa Một Cột'."
        )
    )
    is_text: bool = Field(description="True nếu là ảnh có chữ, False nếu không phải")
    text_content: str = Field(description="Nội dung chữ trong ảnh")


llm = ChatGoogleGenerativeAI(
    model=LLM_MODEL, google_api_key=os.getenv("GOOGLE_API_KEY"), temperature=0.3
)

structured_llm = llm.with_structured_output(ImageVisionResult)
