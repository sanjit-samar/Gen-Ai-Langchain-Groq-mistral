from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage


load_dotenv()

llm = ChatMistralAI(model="mistral-small-2603", temperature=0)

messages = [SystemMessage(content="You are a professional AI agent")]

print("--- welcome to this chat bot, Press 0 to exit the chat!")

while True:
    prompt = input("YOU: ")
    messages.append(HumanMessage(content=prompt))

    if prompt == "0":
        break
    response = llm.invoke(messages)
    messages.append(AIMessage(content=response.content))
    print("BOT :", response.content)
