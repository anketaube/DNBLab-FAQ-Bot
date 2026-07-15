import streamlit as st

# Set page config
st.set_page_config(
    page_title="DNBLab FAQ Bot",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Title
st.title("💬 DNBLab FAQ Bot")

# Subtitle
st.markdown(
    """
    <div style="text-align: center; margin-bottom: 30px; font-size: 16px; color: #555;">
        Ihr persönlicher Assistent für Fragen zur Deutschen Nationalbibliothek (DNB) und dem DNBLab.
    </div>
    """,
    unsafe_allow_html=True
)

# Retrieve API key from Streamlit Secrets
api_key = st.secrets["KISSKI_API_KEY"]

# Build the chatbot URL with the API key
chatbot_url = (
    "https://chat-ai.academiccloud.de/chat?"
    "arcana=anke.taube%2FFAQ&"
    "model=qwen3-30b-a3b-instruct-2507&"
    "enable_tools=true&"
    f"api_key={api_key}"
)

# Button to open the chatbot in a new tab
st.markdown(
    f"""
    <div style="text-align: center; margin-top: 20px;">
        <a href="{chatbot_url}" 
           target="_blank" 
           style="display: inline-block; padding: 14px 28px; font-size: 16px; font-weight: 600; color: white; 
                  background-color: #007BFF; border: none; border-radius: 10px; text-decoration: none; 
                  box-shadow: 0 4px 8px rgba(0, 123, 255, 0.2); transition: all 0.3s ease;">
            🔍 Öffne den DNBLab FAQ Bot (Qwen 3 Omni 30B A3B Instruct)
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

# Optional: Add a small description
st.markdown(
    """
    <div style="text-align: center; margin-top: 15px; font-size: 14px; color: #666;">
        Der Bot basiert auf dem Qwen 3 Omni 30B A3B Instruct Modell von Kisski GWDG.
    </div>
    """,
    unsafe_allow_html=True
)

# Footer
st.markdown(
    """
    <div style="text-align: center; margin-top: 40px; font-size: 12px; color: #999;">
        &copy; 2026 Deutsche Nationalbibliothek | DNBLab | Powered by Kisski GWDG
    </div>
    """,
    unsafe_allow_html=True
)