import os
from langchain_community.document_loaders import PyPDFLoader
from utils.utils import get_docs_user_upload_files


class Loader:
    def __init__(self):
        self.folder = os.path.dirname(os.path.dirname(__file__)) + "/data"
        self.docs = []
        self.user_docs = []

    def load_system_documents(self):
        for file in os.listdir(self.folder):
            if file.endswith(".pdf"):
                path = os.path.join(self.folder, file)
                print("Loading document : ", file)
                loader = PyPDFLoader(path)
                self.docs.extend(loader.load())

        return self.docs

    def load_uploaded_documents(self, upload_files):
        for file in upload_files:
            docs = get_docs_user_upload_files(file)
            self.user_docs.extend(docs)
        return self.user_docs
