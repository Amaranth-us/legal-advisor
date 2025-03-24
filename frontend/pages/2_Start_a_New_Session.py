import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv("BACKEND_URL")

st.title("Legal Advisor AI Chatbot")

st.write(
    "Ask your legal questions, and receive AI-generated responses based on general legal information. "
    "You can also view the history of your previous conversations."
)

if st.button("New Session"):
    try:
        session_response = requests.get(f"{backend_url}/highest-session-id")

        if session_response.status_code == 200:
            # highest_session_id = int(session_response.text.strip('"'))
            highest_session_id = int(session_response.text)
            new_session_id = str(highest_session_id + 1)

            st.session_state.new_session_id = new_session_id
            st.session_state.chat_history = []

            st.write(f"New session started with session ID: {new_session_id}")
        else:
            st.error("Error: Unable to fetch the highest session ID.")
    except Exception as e:
        st.error(f"An error occurred while fetching session data: {e}")

if "new_session_id" in st.session_state:
    st.subheader("Chat History for Current Session")

    if st.session_state.chat_history:
        for entry in st.session_state.chat_history:
            st.write(f"**Role:** {entry['role']}")
            st.write(f"**Content:** {entry['content']}")
            st.write(f"**Timestamp:** {entry['timestamp']}")
            st.write("-" * 50)
    else:
        st.write("No chat history yet.")

    question = st.text_input("Enter your legal advice prompt:")

    if st.button("Ask"):
        if question:
            payload = {"question": question}

            try:
                response = requests.post(
                    f"{backend_url}/chat/{st.session_state.new_session_id}",
                    json=payload,
                )

                if response.status_code == 200:
                    answer = response.json().get("answer", "No answer received.")
                    st.write(f"**Answer:** {answer}")

                    st.session_state.chat_history.append(
                        {
                            "role": "user",
                            "content": question,
                            "timestamp": "Just now",
                        }
                    )

                    st.session_state.chat_history.append(
                        {
                            "role": "assistant",
                            "content": answer,
                            "timestamp": "Just now",
                        }
                    )

                else:
                    st.error("Error: Unable to get a response from the backend.")
            except Exception as e:
                st.error(f"An error occurred while contacting the backend: {e}")
        else:
            st.warning("Please enter a question.")
else:
    st.write("Click 'New Session' to start a new session.")
