import os
from langchain_community.document_loaders import PyPDFLoader
class Loader:
    def __init__(self):
        self.folder = os.path.dirname(os.path.dirname(__file__)) + "/data"
        self.docs = []
    
    def load_documents(self):
        for file in os.listdir(self.folder):
            if file.endswith(".pdf"):
                path = os.path.join(self.folder, file)
                print("Loading document : ",file)
                loader = PyPDFLoader(path)
                self.docs.extend(loader.load())

        return self.docs