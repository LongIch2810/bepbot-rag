import os
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import LLM_MODEL
from dotenv import load_dotenv

load_dotenv()


class FileValidationResult(BaseModel):
    is_food_related: bool = Field(description="Có liên quan ẩm thực không")
    content: str = Field(description="Chủ đề mà nội dung này mô tả")


llm = ChatGoogleGenerativeAI(
    model=LLM_MODEL, google_api_key=os.getenv("GOOGLE_API_KEY"), temperature=0.3
)

structured_llm = llm.with_structured_output(FileValidationResult)
