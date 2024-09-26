import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
from streamlit_lottie import st_lottie
import requests
import random
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Cosmic Chat with Gemini-Pro",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
        
        body {
            background-color: #0a192f;
            color: #8892b0;
            font-family: 'Orbitron', sans-serif;
        }
        .stChatMessage.user {
            background-color: rgba(100, 255, 218, 0.1);
            border-radius: 15px;
            padding: 15px;
            border-left: 5px solid #64ffda;
            margin-bottom: 15px;
            animation: glow 1.5s ease-in-out infinite alternate;
        }
        .stChatMessage.assistant {
            background-color: rgba(255, 100, 218, 0.1);
            border-radius: 15px;
            padding: 15px;
            border-left: 5px solid #ff64da;
            margin-bottom: 15px;
            animation: glow 1.5s ease-in-out infinite alternate;
        }
        .stTitle {
            color: #64ffda;
            text-align: center;
            font-size: 3rem;
            font-weight: bold;
            text-shadow: 0 0 10px #64ffda, 0 0 20px #64ffda, 0 0 30px #64ffda;
        }
        .stTextInput>div>div>input {
            border-radius: 25px;
            border: 2px solid #64ffda;
            background-color: rgba(100, 255, 218, 0.1);
            color: #64ffda;
        }
        .stButton>button {
            border-radius: 25px;
            background-color: #64ffda;
            color: #0a192f;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: scale(1.05);
            box-shadow: 0 0 15px #64ffda;
        }
        .sidebar .stButton>button {
            background-color: #ff64da;
        }
        @keyframes glow {
            from {
                box-shadow: 0 0 5px rgba(100, 255, 218, 0.5);
            }
            to {
                box-shadow: 0 0 20px rgba(100, 255, 218, 0.8);
            }
        }
        footer {
            visibility: hidden;
        }
    </style>
""", unsafe_allow_html=True)

# API key for Google Generative AI
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Function to translate roles
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Function to load Lottie animation
def load_lottieurl(url: str):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

# Initialize chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Sidebar
with st.sidebar:
    st.title("🛸 Cosmic Controls")
    temperature = st.slider("AI Cosmic Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
    max_tokens = st.number_input("Max Stardust Tokens", min_value=50, max_value=1000, value=250, step=50)
    
    if st.button("🌠 Generate Random Space Fact"):
        space_facts = [
            "A year on Venus is shorter than its day.",
            "Neutron stars can spin at a rate of 600 rotations per second.",
            "There is a planet made of diamonds twice the size of Earth.",
            "The footprints on the Moon will last for 100 million years.",
            "The largest known star, UY Scuti, is 1,700 times wider than the Sun."
        ]
        st.session_state.space_fact = random.choice(space_facts)

# Main content
st.title("🌌 Cosmic Gemini - Your Galactic AI Guide")

col1, col2 = st.columns([2, 1])

with col1:
    # Chat interface
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    user_prompt = st.chat_input("Ask the cosmos... 🌠")

    if user_prompt:
        st.chat_message("user").markdown(user_prompt)
        gemini_response = st.session_state.chat_session.send_message(
            user_prompt,
            generation_config=gen_ai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            )
        )
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)

with col2:
    # Space-themed Lottie animation
    lottie_url = "https://assets9.lottiefiles.com/private_files/lf30_jtkhrafm.json"
    lottie_animation = load_lottieurl(lottie_url)
    st_lottie(lottie_animation, key="lottie", height=300)

    st.markdown("### 🚀 Cosmic Guide:")
    st.markdown("""
    1. Ask your question to the AI in the cosmic input field.
    2. Adjust the AI's cosmic temperature and stardust tokens in the sidebar.
    3. Explore the universe of knowledge with Gemini-Pro!
    """)

    # Display random space fact
    if hasattr(st.session_state, 'space_fact'):
        st.markdown("### 🌟 Cosmic Fact of the Moment:")
        st.info(st.session_state.space_fact)

    # Add a "current time in space" feature
    st.markdown("### 🕰️ Current Time in Deep Space:")
    space_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + " UTC"
    st.code(space_time, language='')

# Easter egg: Hidden message in the stars
if random.random() < 0.1:  # 10% chance to show the easter egg
    st.markdown("""
    <div style='text-align: center; color: #64ffda; font-size: 0.8em; margin-top: 50px;'>
    *whispers of the cosmos* You've discovered a hidden message in the stars! 🌟
    </div>
    """, unsafe_allow_html=True)
