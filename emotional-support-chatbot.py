import streamlit as st
import openai
import time
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Apoyo Emocional - Chatbot Terapéutico",
    page_icon="💭",
    layout="centered"
)

# CSS for styling the chat interface
st.markdown("""
<style>
    .chat-container {
        border-radius: 10px;
        margin-bottom: 20px;
        padding: 20px;
        background-color: #f5f5f7;
    }
    .user-message {
        background-color: #DCF8C6;
        border-radius: 15px;
        padding: 10px 15px;
        margin: 5px 0;
        max-width: 80%;
        margin-left: auto;
        text-align: right;
    }
    .bot-message {
        background-color: #FFFFFF;
        border-radius: 15px;
        padding: 10px 15px;
        margin: 5px 0;
        max-width: 80%;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    .header {
        color: #4A4A4A;
        margin-bottom: 20px;
        text-align: center;
    }
    .footer {
        text-align: center;
        font-size: 12px;
        color: #888;
        margin-top: 30px;
    }
    .stTextInput>div>div>input {
        border-radius: 20px;
    }
    .quote {
        border-left: 3px solid #7D7D7D;
        padding-left: 10px;
        font-style: italic;
        color: #555;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# App title and description
st.markdown("<h1 class='header'>Compañero Emocional</h1>", unsafe_allow_html=True)
st.markdown("""
<div class='chat-container'>
<p>Este chatbot está diseñado para apoyarte durante momentos de crisis emocional, 
pensamientos intrusivos o dificultades relacionadas con la dependencia emocional y el apego ansioso.</p>

<p>Recuerda: <b>Este chatbot no sustituye la terapia profesional.</b> 
Si estás experimentando dificultades emocionales significativas, 
te recomendamos buscar ayuda de un profesional de la salud mental.</p>

<div class='quote'>
"El primer paso hacia el cambio es la conciencia. El segundo paso es la aceptación."
</div>
</div>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# OpenAI API key input
with st.sidebar:
    
    st.header("Sobre este chatbot")
    st.markdown("""
    Este chatbot utiliza inteligencia artificial para ofrecer apoyo emocional 
    durante momentos difíciles relacionados con:
    
    - Dependencia emocional
    - Apego ansioso
    - Crisis emocionales
    - Pensamientos intrusivos
    - Ansiedad en relaciones
    
    Siempre consulta con un terapeuta profesional para recibir ayuda adecuada.
    """)
    
    st.markdown("### Desarrollado por")
    st.markdown("<div style='text-align:center;'><b>Paola Espino</b></div>", unsafe_allow_html=True)

# Chat prompt engineering
system_prompt = st.secrets.system_prompt

# Set OpenAI API key
client = openai.OpenAI(api_key=st.secrets.openai_api_key)

# Prompt for new input and handle response
if prompt := st.chat_input("Cómo te sientes hoy?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.markdown("""
<div class='footer'>
    <p>Este chatbot es una herramienta de apoyo y no sustituye la terapia profesional.</p>
    <p>© 2025 Desarrollado por Paola Espino | Última actualización: Abril 2025</p>
</div>
""", unsafe_allow_html=True)
