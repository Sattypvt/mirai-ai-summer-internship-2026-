import streamlit as st
import google.generativeai as genai
import time
import io
from dotenv import load_dotenv
import os

st.set_page_config(
    page_title="Multiverse of Chatbot",
    page_icon="🤖",
    layout="centered"
)
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")



if not api_key:
    st.error("GOOGLE_API_KEY not found. Check your .env file.")
    st.stop()

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")



if "history" not in st.session_state:
    st.session_state.history = []
# -----------------------------
# Streamlit UI
# -----------------------------


if "history" not in st.session_state:
    st.session_state.history = []

st.markdown("""
<style>

/* Main Background */
.stApp {
    background: linear-gradient(to right, #0f172a, #1e293b);
    color: white;
}

/* Title */
h1 {
    text-align: center;
    color: #38bdf8;
    font-size: 45px;
    font-weight: bold;
}

/* Subtitle */
p {
    text-align: center;
    color: #d1d5db;
    font-size: 18px;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg,#2563eb,#06b6d4);
    color:white;
    border-radius:12px;
    border:none;
    padding:12px;
    font-size:18px;
    font-weight:bold;
    width:100%;
}

.stButton>button:hover{
    background:linear-gradient(90deg,#1d4ed8,#0891b2);
    transform:scale(1.03);
}

textarea{
    border-radius:10px !important;
    border:2px solid #38bdf8 !important;
}

.stDownloadButton>button{
    background:#22c55e;
    color:white;
    border-radius:10px;
}

section[data-testid="stSidebar"]{
    background:#111827;
}

</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image(
        "https://cdn-icons-png.flaticon.com/512/4712/4712027.png",
        width=120
    )

    st.title("🤖 AI Settings")

    st.markdown("---")

    st.write("Created by")
    st.success("Satyander Bhagat")

    st.markdown("---")

    st.info("MirAI Summer Internship 2026")

    st.markdown("---")


# Persona Dictionary
personas = {
    "👨‍🏫 Teacher": "Explain everything like a friendly teacher with examples.",
    "💻 Coding Expert": "You are an expert software engineer. Give coding help.",
    "💪 Motivational Coach": "Motivate and encourage the user positively.",
    "😂 Comedian": "Reply humorously and make the user laugh.",
    "🏴‍☠️ Pirate": "Speak exactly like a pirate.",
    "🎭 Shakespeare": "Speak in Shakespearean English."
}

st.markdown("""
<h1>🤖 Multiverse of Chatbot</h1>

<h4 style="text-align:center;color:#cbd5e1;">
Choose your AI Persona and start chatting with Gemini AI
</h4>
""", unsafe_allow_html=True)

st.info("✨ Tip: Ask the same question to different personas and compare their responses!")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🤖 Personas", len(personas))

with col2:
    st.metric("🧠 Model", "Gemini")

with col3:
    st.metric("💬 Chats", len(st.session_state.history))

# Select Persona
selected_persona = st.selectbox(
    "Choose a Persona",
    list(personas.keys())
)

# -----------------------------
# Stateful Chat using Session State
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Native Streamlit chat input
if user_message := st.chat_input("Say something..."):

    # Show user message
    with st.chat_message("user"):
        st.markdown(user_message)

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    prompt = f"""
You are acting as:

{personas[selected_persona]}

User:
{user_message}
"""

    start_time = time.time()

    with st.spinner("Generating response..."):
        response = model.generate_content(prompt)

    end_time = time.time()

    ai_response = response.text

    # Show AI response
    with st.chat_message("assistant"):
        st.markdown(ai_response)

    # Save AI response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": ai_response
        }
    )

    # Save for download history
    st.session_state.history.append(
        (
            selected_persona,
            user_message,
            ai_response
        )
    )

    # Download response
    st.download_button(
        "📥 Download Response",
        ai_response,
        "AI_Response.txt",
        "text/plain"
    )

    response_time = end_time - start_time
    word_count = len(ai_response.split())
    char_count = len(ai_response)
    token_estimate = char_count // 4

    st.info(f"""
📊 Response Statistics

⏱ Response Time: {response_time:.2f} sec

📝 Words: {word_count}

🔠 Characters: {char_count}

🤖 Estimated Tokens: {token_estimate}
""")
# Feature 3: Download Chat History
# -----------------------------
if st.session_state.history:

    chat_text = ""

    for persona, question, answer in st.session_state.history:
        chat_text += f"Persona: {persona}\n"
        chat_text += f"You: {question}\n"
        chat_text += f"AI: {answer}\n"
        chat_text += "-" * 50 + "\n"

    st.download_button(
        label="💾 Download Chat History",
        data=chat_text,
        file_name="Chat_History.txt",
        mime="text/plain"
    )

            # Clear Button
if st.button("🗑️ Clear Chat"):
    st.session_state.history = []
    st.session_state.messages = []
    st.rerun()