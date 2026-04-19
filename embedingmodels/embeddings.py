from langchain_openai import OpenAIEmbeddings
from langchain_mistralai import MistralAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-large", dimensions=64)
# embeddings = MistralAIEmbeddings(model="mistral-embed", dimensions=64)

# vector = embeddings.embed_query("you are great")

texts = [
    "Where is the Silicon valley in USA",
    "How many employees are working with microsoft",
    "where is the capital of UK",
]

vector = embeddings.embed_documents(texts)

print(vector)
