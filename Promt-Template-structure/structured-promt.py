from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import List, Optional

load_dotenv()

llm = ChatMistralAI(model="mistral-small-2603")


class Movie(BaseModel):
    title: str
    description: str
    Genre: List[str]
    year: Optional[int]
    cast: List[str]
    rating: Optional[float]
    director: Optional[str]


parser = PydanticOutputParser(pydantic_object=Movie)

chat_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
Extract movie information from the paragraph
    {format_instructions}
""",
        ),
        ("human", "{movie_description}"),
    ]
)

Ip_para = input("Give your Movie Para : ")

final_promt = chat_prompt.invoke(
    {
        "movie_description": Ip_para,
        "format_instructions": parser.get_format_instructions(),
    }
)

response = llm.invoke(final_promt)

# structured_response = parser.parse(response.content)

raw_content = response.content.strip()

# Remove code block markers if present
if raw_content.startswith("```json"):
    raw_content = raw_content[len("```json") :].strip()
if raw_content.startswith("```"):
    raw_content = raw_content[len("```") :].strip()
if raw_content.endswith("```"):
    raw_content = raw_content[:-3].strip()

print(raw_content)
