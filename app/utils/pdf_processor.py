from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.vectorstores.base import VectorStoreRetriever
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app import chroma_client, config


class PDFProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.__validate_file()
        self.__embedding_function = OllamaEmbeddings(model=config.MODEL_NAME)
        self.collection_name = (
            f"file_{file_path.split('/')[-1].split('.')[0]}_collection"
        )

    def __validate_file(self) -> bool:
        if not self.file_path.endswith(".pdf"):
            raise ValueError("Invalid file type. Please upload a PDF file.")
        return True

    def pdf_indexing(self) -> list:
        loader = PyPDFLoader(self.file_path)
        documents = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        return splitter.split_documents(documents)

    def get_or_create_collection(self) -> Chroma:
        existing = [c.name for c in chroma_client.list_collections()]
        if self.collection_name in existing:
            collection = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.__embedding_function,
                client=chroma_client,
            )
            return collection

        chunked_documents = self.pdf_indexing()
        collection = Chroma.from_documents(
            documents=chunked_documents,
            embedding=self.__embedding_function,
            collection_name=self.collection_name,
            client=chroma_client,
        )
        return collection

    def as_retriever(self)-> VectorStoreRetriever:
        vector_store = self.get_or_create_collection()
        retriever = vector_store.as_retriever(
            search_type="similarity", search_kwargs={"k": 5}
        )

        return retriever
