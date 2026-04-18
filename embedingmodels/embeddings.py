from langchain_openai import OpenAIEmbeddings
from langchain_mistralai import MistralAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-large", dimensions=64)
# embeddings = MistralAIEmbeddings(model="mistral-embed", dimensions=64)

vector = embeddings.embed_query("you are great")

print(vector)
