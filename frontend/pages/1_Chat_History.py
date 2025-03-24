import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv("BACKEND_URL")

st.title("Legal Advisor AI Chatbot History")

st.subheader("Find your session history in here. ")


# session_id = st.text_input("Enter Session ID to view history:")

# if st.button("Get Chat History1"):
#     if session_id:
#         try:
#             history_response = requests.get(f"{backend_url}/chat-history/{session_id}")

#             if history_response.status_code == 200:
#                 chat_history = history_response.json()
#                 if chat_history:
#                     for entry in chat_history:
#                         st.write(f"**Role:** {entry['role']}")
#                         st.write(f"**Content:** {entry['content']}")
#                         st.write(f"**Timestamp:** {entry['timestamp']}")
#                         st.write("-" * 50)
#                 else:
#                     st.write("No chat history found for this session.")
#             else:
#                 st.error("Error: Unable to retrieve chat history.")
#         except Exception as e:
#             st.error(f"An error occurred while retrieving chat history: {e}")
#     else:
#         st.warning("Please enter a valid session ID.")


try:
    session_response = requests.get(f"{backend_url}/chat-sessions")
    if session_response.status_code == 200:
        sessions = session_response.json()

        if sessions:
            session_selected = st.selectbox(
                "Select a session to view chat history:",
                [
                    f"{session['session_id']} - {session['oldest_timestamp']}"
                    for session in sessions
                ],
            )

            session_id = session_selected.split(" ")[0]

            if session_id:
                history_response = requests.get(
                    f"{backend_url}/chat-history/{session_id}"
                )

                if history_response.status_code == 200:
                    chat_history = history_response.json()
                    if chat_history:
                        for entry in chat_history:
                            st.write(f"**Role:** {entry['role']}")
                            st.write(f"**Content:** {entry['content']}")
                            st.write(f"**Timestamp:** {entry['timestamp']}")
                            st.write("-" * 50)
                    else:
                        st.write("No chat history found for this session.")
                else:
                    st.error("Error: Unable to retrieve chat history.")
        else:
            st.write("No sessions available.")
    else:
        st.error("Error: Unable to fetch session data.")
except Exception as e:
    st.error(f"An error occurred while fetching session data: {e}")
