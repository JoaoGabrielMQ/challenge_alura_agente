from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()
caminho_da_pasta = "./documentos"

loader = DirectoryLoader(path=caminho_da_pasta,
                         glob="**/*.pdf",
                         loader_cls=PyPDFLoader,
                         show_progress=True)

paginas_originais = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=600,
                                               chunk_overlap=100)

meus_documentos = text_splitter.split_documents(paginas_originais)

for doc in meus_documentos:
    if not doc.page_content.startswith("passage: "):
        doc.page_content = f"passage: {doc.page_content}"

modelo_embedding = HuggingFaceEmbeddings(model_name="google/embeddinggemma-300m", encode_kwargs={"prompt": "query: "})

vector_store = InMemoryVectorStore.from_documents(documents=meus_documentos, embedding=modelo_embedding)
