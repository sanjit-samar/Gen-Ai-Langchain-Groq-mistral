from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st

load_dotenv()

st.title("Movie Information Extractor")

llm = ChatMistralAI(model="mistral-small-2603")

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

Ip_para = st.text_area("Give your Movie Para :")

if st.button("Extract"):
    if Ip_para.strip():
        with st.spinner("Extracting movie information..."):
            final_promt = chat_prompt.invoke({"movie_description": Ip_para})
            response = llm.invoke(final_promt)
            st.write(response.content)
    else:
        st.warning("Please enter a movie description.")
