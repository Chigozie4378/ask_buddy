from dotenv import load_dotenv
from langchain_cohere import CohereEmbeddings
from langchain_community.document_loaders.text import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS

load_dotenv()
loader = TextLoader('text.txt', encoding='utf8')
text_documents = loader.load()
from langchain_community.document_loaders import DirectoryLoader
loader = DirectoryLoader('./data', glob="**/*.pdf",loader_cls=PyPDFLoader, show_progress=True)
docs = loader.load()

# Splitting
from langchain_text_splitters import RecursiveCharacterTextSplitter
splitter = RecursiveCharacterTextSplitter(
    separators=['\n\n','\n',' ','.'],
    chunk_size=1500,
    chunk_overlap=300,
)
splits = splitter.split_documents(docs)

# Embeddings
embeddings = CohereEmbeddings()

# Vector Index
vector_index = FAISS.from_documents(splits, embeddings)
vector_index.save_local('faiss_store')

# vector_index = FAISS.load_local("faiss_store", CohereEmbeddings(), allow_dangerous_deserialization=True)
# retrieval = vector_index.as_retriever()
# response = retrieval.invoke(" what are the steps to draw an Aufbau diagram")

# print(response)