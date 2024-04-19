import dotenv

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Load environment variables
dotenv.load_dotenv()

# Create LLM
llm = ChatOpenAI(model="gpt-3.5-turbo")

loader = PyPDFLoader("data/USA_Pickleball_Rulebook_2024_v1.pdf")
pages = loader.load_and_split()

create_new_vectors = False

# Save vectors to disk
if create_new_vectors:
    vectorstore = Chroma.from_documents(documents=pages, embedding=OpenAIEmbeddings(), persist_directory="./chroma_db")

# Load vectors to disk
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=OpenAIEmbeddings())