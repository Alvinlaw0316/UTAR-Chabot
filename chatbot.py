import streamlit as st
from rapidfuzz import process
import json
import os
import re

# --- Load FAQ database ---
script_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(script_dir, "utar_faq.json")

try:
    with open(json_path, "r", encoding="utf-8") as f:
        faq_responses = json.load(f)
except FileNotFoundError:
    st.error("❌ FAQ database JSON file not found.")

# --- Small talk responses ---
small_talk = {
    "hello": "👋 Hi there! Do you have any questions about UTAR Kampar?",
    "how are you": "😊 I'm good! How can I assist you with UTAR today?",
    "good morning": "🌞 Good morning! What UTAR info can I help you with today?",
    "good afternoon": "☀️ Good afternoon! Need any info about UTAR Kampar?",
    "good evening": "🌙 Good evening! How can I assist you today?",
    "who are you": "🤖 I'm UTAR Kampar Chatbot! I'm here to help you with campus info, like library hours, exams, clubs, and more."
}

# --- Helper function to normalize text ---
def normalize(text):
    return re.sub(r'[^\w\s]', '', text.lower())

# --- Get chatbot response ---
def get_response(user_input):
    if not user_input.strip():
        return "❓ Please ask me something about UTAR Kampar."

    user_norm = normalize(user_input)

    # Check small talk first
    for key, reply in small_talk.items():
        if key in user_norm:
            return reply

    # Then check FAQ
    faq_keys_norm = [normalize(k) for k in faq_responses.keys()]
    best_match, score, index = process.extractOne(user_norm, faq_keys_norm)
    if score > 70:
        original_key = list(faq_responses.keys())[index]
        return faq_responses[original_key]

    # Fallback
    return "🤔 Sorry, I don’t know the answer. Please check the UTAR website or Student Affairs Office."

# --- Streamlit UI ---
st.set_page_config(page_title="UTAR Chatbot", page_icon="🎓", layout="wide")
st.title("🎓 UTAR Kampar Chatbot")
st.write("Ask me anything about UTAR Kampar campus life!")

# --- Session state ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- Chat input form ---
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("💬 Type your question here:")
    submit_button = st.form_submit_button("🚀 Ask")
    
    if submit_button:
        response = get_response(user_input)
        st.session_state.history.append(("You", user_input))
        st.session_state.history.append(("Chatbot", response))

# --- Chat container ---
st.subheader("Chat History")
for role, message in st.session_state.history:
    st.write(f"**{role}:** {message}")
