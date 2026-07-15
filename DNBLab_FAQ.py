import streamlit as st
import requests
import json

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
API_KEY = st.secrets["KISSKI_API_KEY"]

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
        try:
            with st.spinner("Antwort wird generiert..."):
                response = requests.post(API_URL, json=payload, timeout=30)
                if response.status_code != 200:
                    st.error(f"❌ Fehler: {response.status_code} - {response.text}")
                    st.session_state.messages.append({"role": "assistant", "content": f"Fehler: {response.status_code} - {response.text}"})
                else:
                    # Parse JSON response
                    data = response.json()
                    if "message" in data:
                        full_response = data["message"]
                        st.markdown(full_response)
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
                    else:
                        st.error("❌ Keine Antwort im API-Response gefunden.")
                        st.session_state.messages.append({"role": "assistant", "content": "Keine Antwort erhalten."})
        except Exception as e:
            st.error(f"❌ Fehler beim Abrufen der Antwort: {str(e)}")
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
