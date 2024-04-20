import dotenv

from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Load environment variables
dotenv.load_dotenv()

# Create LLM
llm = ChatOpenAI(model="gpt-3.5-turbo")

# To create new vectors and save to disk, set this to True
create_new_vectors = False

if create_new_vectors:
    loader = PyPDFLoader("data/USA_Pickleball_Rulebook_2024_v1.pdf")
    pages = loader.load_and_split()
    vectorstore = Chroma.from_documents(documents=pages, embedding=OpenAIEmbeddings(), persist_directory="./chroma_db")

# Load vectors to disk
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=OpenAIEmbeddings())

# Retrieve and generate using the relevant snippets of the rulebook
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
prompt = hub.pull("rlm/rag-prompt")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

def rag_chain_function(input_text: str):
    return rag_chain.invoke(input_text)