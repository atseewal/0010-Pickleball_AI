import dotenv

# Load environment variables
dotenv.load_dotenv()

from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("data/USA_Pickleball_Rulebook_2024_v1.pdf")
pages = loader.load_and_split()