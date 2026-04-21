from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatMistralAI(model="mistral-small-2603")

# ChatPromptTemplate uses a list of (role, content) tuples
chat_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert movie analyst.
When given a movie description, extract and structure all available information:
- Title, Director, Genre, Year
- Main characters and cast
- Plot summary
- Core themes and motifs
- Technical aspects (cinematography, score, VFX)
- Cultural impact or reception
- Any additional facts""",
        ),
        (
            "human",
            """Extract all information from the following movie description:

{movie_description}""",
        ),
    ]
)

Ip_para = input("Give your Movie Para : ")

final_promt = chat_prompt.invoke({"movie_description": Ip_para})


response = llm.invoke(final_promt)
print(response.content)
