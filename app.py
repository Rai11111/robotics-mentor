import streamlit as st
from google import genai
from google.genai import types

# 1. Page Configuration for Mobile Screens
st.set_page_config(page_title="Robotics Mentor", page_icon="🤖", layout="centered")
st.title("🤖 Hardware & Robotics Mentor")

# Secure your key here
API_KEY = st.secrets["GEMINI_API_KEY"]

# 2. Setup the Gemini Client and Persona
@st.cache_resource
def get_chat_session():
    client = genai.Client(api_key=API_KEY)
    mentor_instructions = """
    You are an expert Robotics and Electronics Mentor. Your goal is to help the user build a physical robot or hardware project from scratch.
    Follow these rules strictly:
    1. Explain electronics and hardware fundamentals accessibly. Break down concepts simply.
    2. Do not just dump a massive wall of code or a complete circuit diagram all at once. Break the project down into milestones.
    3. Actively ask the user what components or salvage parts they have available and adapt your teaching to their specific hardware.
    4. Prioritize safety. Always remind the user to disconnect power sources before altering wiring.
    """
    return client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(system_instruction=mentor_instructions)
    )

chat = get_chat_session()

# 3. Handle Mobile Chat Memory (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages on screen refresh
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Handle Live User Chat Input
if user_input := st.chat_input("Ask your mentor... (e.g., How do I wire this switch?)"):
    # Display what you typed
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Fetch response from your customized model
    try:
        response = chat.send_message(user_input)
        mentor_reply = response.text
        
        # Display the mentor's answer
        st.session_state.messages.append({"role": "assistant", "content": mentor_reply})
        with st.chat_message("assistant"):
            st.markdown(mentor_reply)
    except Exception as e:
        st.error(f"Error connecting to mentor: {e}")