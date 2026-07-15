import streamlit as st
import requests
import json
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="DNBLab FAQ Bot",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Title
st.title("💬 DNBLab FAQ Bot")
st.markdown(
    """
    <div style="text-align: center; font-size: 14px; color: #666;">
        Ihr persönlicher Assistent für Fragen zur Deutschen Nationalbibliothek (DNB) und dem DNBLab.  
        <br>Modell: <strong>Qwen 3 Omni 30B A3B Instruct</strong> (Kisski GWDG)
    </div>
    """,
    unsafe_allow_html=True
)

# --- API Configuration ---
API_URL = "https://chat-ai.academiccloud.de/chat"
API_KEY = st.secrets["KISSKI_API_KEY"]  # Securely loaded from Streamlit Secrets

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display Chat Messages ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- User Input ---
if prompt := st.chat_input("Stellen Sie Ihre Frage zum DNBLab oder zur DNB..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare API request
    payload = {
        "arcana": "anke.taube%2FFAQ",
        "model": "qwen3-30b-a3b-instruct-2507",
        "enable_tools": True,
        "api_key": API_KEY,
        "messages": [
            {"role": "system", "content": "Sie sind ein hilfreicher Assistent für die Deutsche Nationalbibliothek (DNB) und das DNBLab. Beantworten Sie Fragen präzise und basierend auf den verfügbaren Daten."}
        ] + [
            {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
        ]
    }

    # Send request to Kisski GWDG API
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            with requests.post(API_URL, json=payload, stream=True) as response:
                if response.status_code != 200:
                    message_placeholder.markdown(f"❌ Fehler: {response.status_code} - {response.text}")
                    st.session_state.messages.append({"role": "assistant", "content": f"Fehler: {response.status_code} - {response.text}"})
                else:
                    for chunk in response.iter_lines():
                        if chunk:
                            decoded_chunk = chunk.decode('utf-8')
                            if decoded_chunk.startswith("data: "):
                                try:
                                    json_data = json.loads(decoded_chunk[5:])
                                    if "message" in json_data:
                                        full_response += json_data["message"]
                                        message_placeholder.markdown(full_response + "▌")
                                except:
                                    continue
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            message_placeholder.markdown(f"❌ Fehler beim Abrufen der Antwort: {str(e)}")
            st.session_state.messages.append({"role": "assistant", "content": f"Fehler: {str(e)}"})

# --- Footer ---
st.markdown(
    """
    <div style="text-align: center; margin-top: 40px; font-size: 12px; color: #999;">
        &copy; 2026 Deutsche Nationalbibliothek | DNBLab | Powered by Kisski GWDG
    </div>
    """,
    unsafe_allow_html=True
)
