from dotenv import load_dotenv

# init_chat_model = It is shortcut or wrapper class where we need to mention only model name
from langchain.chat_models import init_chat_model
from langchain_groq import ChatGroq
from langchain_mistralai import ChatMistralAI

load_dotenv()

# groq_llm = ChatGroq(model="llama-3.3-70b-versatile")
# groq_llm = init_chat_model("llama-3.3-70b-versatile",model_provider="groq")

mistral_llm = ChatMistralAI(model="mistral-small-2603")

# response = groq_llm.invoke("What is full stack Ai engineeer role ?")
response = mistral_llm.invoke("what are huggingface embedding models ?")

print(response.content)
