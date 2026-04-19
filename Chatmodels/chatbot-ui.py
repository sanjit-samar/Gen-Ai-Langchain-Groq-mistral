import streamlit as st
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

# Load environment variables
load_dotenv()

# Initialize model
llm = ChatMistralAI(model="mistral-small-2603", temperature=0)

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content="You are a professional AI agent")
    ]

st.title("💬 Mistral Chatbot")
st.write("Welcome to this chatbot. Type '0' to exit (clears chat).")

# Chat input
user_input = st.text_input("YOU:", key="chat_input")

if user_input:
    if user_input.strip() == "0":
        st.session_state.messages = [
            SystemMessage(content="You are a professional AI agent")
        ]
        st.success("Chat cleared. Start again!")
    else:
        # Append user message
        st.session_state.messages.append(HumanMessage(content=user_input))

        # Get response
        response = llm.invoke(st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=response.content))

# Display chat history
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        st.markdown(f"**YOU:** {msg.content}")
    elif isinstance(msg, AIMessage):
        st.markdown(f"**BOT:** {msg.content}")
