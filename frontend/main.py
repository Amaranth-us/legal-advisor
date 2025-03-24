import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


BACKEND_URL = os.getenv("BACKEND_URL")


st.title("Legal Advisor AI Chatbot")


st.write(
    "Ask your legal questions, and receive AI-generated responses based on general legal information. "
    "You can also view the history of your previous conversations."
)


question = st.text_input("Enter your legal question:")

if st.button("Get Answer"):
    if question:
        payload = {"question": question}

        try:
            response = requests.post(f"{BACKEND_URL}/chat", json=payload)

            if response.status_code == 200:
                answer = response.json().get("answer", "No answer received.")
                st.write(f"**Answer:** {answer}")
            else:
                st.error("Error: Unable to get a response from the backend.")
        except Exception as e:
            st.error(f"An error occurred while contacting the backend: {e}")
    else:
        st.warning("Please enter a question.")
