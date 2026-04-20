from app.workflow import Workflow
from app.config import SYSTEM_ONLY


def main():
    print("=== Chatbot RAG Công Thức Nấu Ăn Việt Nam ===")
    print("Đang khởi tạo hệ thống...")

    try:
        workflow = Workflow()
        workflow.load_and_process_documents()
        print("Hệ thống đã sẵn sàng.")
        print("Nhập 'exit' hoặc 'quit' để thoát.\n")

        while True:
            query = input("Bạn: ").strip()

            if not query:
                print("Vui lòng nhập câu hỏi.")
                continue

            if query.lower() in ["exit", "quit"]:
                print("Tạm biệt!")
                break

            try:
                answer = workflow.retriever_and_generattion(query, SYSTEM_ONLY)
                print(f"Bot: {answer}\n")
            except Exception as e:
                print(f"Lỗi khi truy vấn: {e}\n")

    except Exception as e:
        print(f"Lỗi khởi tạo hệ thống: {e}")


if __name__ == "__main__":
    main()
