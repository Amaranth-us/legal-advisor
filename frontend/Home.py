import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv("BACKEND_URL")

st.title("Legal Advisor AI Chatbot")

st.write(
    "Ask your legal questions, and receive AI-generated responses based on general legal information. "
    "You can also view the history of your previous conversations."
)
