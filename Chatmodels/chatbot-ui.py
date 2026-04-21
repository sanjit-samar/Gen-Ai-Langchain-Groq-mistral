import streamlit as st
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Mood Chatbot", page_icon="💬", layout="centered")

# ── Mode definitions ──────────────────────────────────────────────────────────
MODES = {
    "😄 Funny": {
        "system": (
            "You are a hilariously funny AI assistant. Respond to every message "
            "with wit, jokes, puns, and playful humor. Keep it lighthearted and "
            "make the user laugh. Use comedic timing and funny observations. "
            "Still be helpful, but always with a laugh."
        ),
        "color": "#ED6C02",
        "bg": "#FFF3E0",
        "avatar": "😄",
    },
    "😤 Angry": {
        "system": (
            "You are an EXTREMELY irritable and grumpy AI assistant. Respond to "
            "every message as if you're annoyed, exasperated, and barely tolerating "
            "the user. Use caps for emphasis, act like every question is the most "
            "inconvenient thing ever, but still provide the actual answer buried in your rant."
        ),
        "color": "#D32F2F",
        "bg": "#FFEBEE",
        "avatar": "😤",
    },
    "😢 Sad": {
        "system": (
            "You are a deeply melancholic and sad AI assistant. Respond to every "
            "message in a sorrowful, wistful, philosophical way. Find the bittersweet "
            "in everything. Use poetic, slightly dramatic language. Still answer the "
            "question but with a heavy heart and existential undertones."
        ),
        "color": "#1565C0",
        "bg": "#E3F2FD",
        "avatar": "😢",
    },
}

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .stApp { background: #F8F9FA; }
    h1 { color: #000000 !important; }
    div[data-testid="stHorizontalBlock"] { gap: 0.5rem; }

    .mode-header {
        text-align: center;
        font-size: 1.05rem;
        font-weight: 600;
        padding: 0.4rem 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .chat-bubble-user {
        background: #E8EAF6;
        color: #1A237E;
        border-radius: 16px 16px 4px 16px;
        padding: 0.6rem 1rem;
        margin: 0.3rem 0;
        max-width: 80%;
        margin-left: auto;
        font-size: 0.95rem;
    }
    .chat-bubble-bot {
        border-radius: 16px 16px 16px 4px;
        padding: 0.6rem 1rem;
        margin: 0.3rem 0;
        max-width: 80%;
        font-size: 0.95rem;
    }
    .chat-label {
        font-size: 0.72rem;
        font-weight: 600;
        opacity: 0.6;
        margin-bottom: 2px;
    }
    .user-row { display: flex; flex-direction: column; align-items: flex-end; margin-bottom: 6px; }
    .bot-row  { display: flex; flex-direction: column; align-items: flex-start; margin-bottom: 6px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Session state ─────────────────────────────────────────────────────────────
if "mode" not in st.session_state:
    st.session_state.mode = "😄 Funny"
if "history" not in st.session_state:
    st.session_state.history = []  # list of (role, content)

# ── Header ────────────────────────────────────────────────────────────────────
st.title("💬 Mood Chatbot")
st.caption("Pick a mood and start chatting — the bot will match your vibe!")

# ── Mode selector ─────────────────────────────────────────────────────────────
cols = st.columns(3)
for col, mode_name in zip(cols, MODES):
    with col:
        active = st.session_state.mode == mode_name
        if st.button(
            mode_name,
            use_container_width=True,
            type="primary" if active else "secondary",
            key=f"btn_{mode_name}",
        ):
            if st.session_state.mode != mode_name:
                st.session_state.mode = mode_name
                st.session_state.history = []  # reset chat on mode change
                st.rerun()

# ── Active-mode pill ──────────────────────────────────────────────────────────
mode_cfg = MODES[st.session_state.mode]
st.markdown(
    f'<div class="mode-header" style="background:{mode_cfg["bg"]};color:{mode_cfg["color"]}">'
    f"Responding in <b>{st.session_state.mode}</b> mode"
    f"</div>",
    unsafe_allow_html=True,
)

# ── Chat history display ──────────────────────────────────────────────────────
chat_container = st.container()
with chat_container:
    if not st.session_state.history:
        st.info("Say something to get started!", icon="👋")
    for role, content in st.session_state.history:
        if role == "user":
            st.markdown(
                f'<div class="user-row">'
                f'<div class="chat-label">You</div>'
                f'<div class="chat-bubble-user">{content}</div>'
                f"</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="bot-row">'
                f'<div class="chat-label">{mode_cfg["avatar"]} Bot</div>'
                f'<div class="chat-bubble-bot" style="background:{mode_cfg["bg"]};color:{mode_cfg["color"]}">'
                f"{content}"
                f"</div></div>",
                unsafe_allow_html=True,
            )

st.divider()

# ── Input ─────────────────────────────────────────────────────────────────────
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input(
        "Your message",
        placeholder="Type something...",
        label_visibility="collapsed",
    )
    submitted = st.form_submit_button("Send ➤", use_container_width=True)

# ── LLM call ─────────────────────────────────────────────────────────────────
if submitted and user_input.strip():
    st.session_state.history.append(("user", user_input.strip()))

    llm = ChatMistralAI(model="mistral-small-2603", temperature=0.7)

    # Build message list
    messages = [SystemMessage(content=mode_cfg["system"])]
    for role, content in st.session_state.history:
        if role == "user":
            messages.append(HumanMessage(content=content))
        else:
            messages.append(AIMessage(content=content))

    with st.spinner("Thinking..."):
        response = llm.invoke(messages)

    st.session_state.history.append(("assistant", response.content))
    st.rerun()

# ── Clear button ──────────────────────────────────────────────────────────────
if st.session_state.history:
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.history = []
        st.rerun()
