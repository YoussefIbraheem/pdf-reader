from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app import chroma_client

class PDFProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.__validate_file()
        self.embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        self.collection_name = f"file_{file_path.split('/')[-1].split('.')[0]}_collection"

    def __validate_file(self) -> bool:
        if not self.file_path.endswith(".pdf"):
            raise ValueError("Invalid file type. Please upload a PDF file.")
        return True

    def __pdf_indexing(self) -> list:
        loader = PyPDFLoader(self.file_path)
        documents = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        return splitter.split_documents(documents)

    def __get_or_create_collection(self) -> tuple:
        existing = [c.name for c in chroma_client.list_collections()]
        if self.collection_name in existing:
            collection = Chroma(
                collection_name=self.collection_name,
                embedding=self.embedding_function,
                client=chroma_client,
            )
            return collection , None


        chunked_documents = self.__pdf_indexing()
        collection = Chroma.from_documents(
            documents=chunked_documents,
            embedding=self.embedding_function,
            collection_name=self.collection_name,
            client=chroma_client,
        )
        chroma_client.persist()
        return collection , chunked_documents

    def process_pdf(self) -> tuple:
        """
        Process the PDF file, index its content, and return the collection and chunked documents.
        """
        return self.__get_or_create_collection()