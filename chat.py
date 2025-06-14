import streamlit as st
import groq

MODELOS = ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768"]

def configurar_pagina():
    st.set_page_config(page_title="Mi Chatbot", page_icon="🐐", layout="wide")
    st.title("Bienvenido al chatbot")

def mostrar_sidebar():
    st.sidebar.title("Mis Chats")
    st.sidebar.title("Modelos Disponibles")
    modelo_seleccionado = st.sidebar.selectbox("Elegí tu modelo", MODELOS, index=0)

    if "modelo_actual" not in st.session_state:
        st.session_state.modelo_actual = modelo_seleccionado

    if modelo_seleccionado != st.session_state.modelo_actual:
        st.session_state.mensajes = []  # borrar historial
        st.session_state.modelo_actual = modelo_seleccionado  # actualizar modelo

    st.write(f"**Elegiste el modelo:** {modelo_seleccionado}")
    return modelo_seleccionado

def crear_cliente_groq():
    groq_api_key = st.secrets["GROQ_API_KEY"]
    return groq.Groq(api_key=groq_api_key)

def inicializar_estado_chat():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def obtener_mensajes_previos(): 
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])

def obtener_mensajes_usuario():
    return st.chat_input("Enviá tu mensaje")

def agregar_mensaje(role, content):
    st.session_state.mensajes.append({"role": role, "content": content})

def mostrar_mensaje(role, content):
    with st.chat_message(role):
        st.markdown(content)

def ejecutar_chat():
    configurar_pagina()
    cliente = crear_cliente_groq()
    inicializar_estado_chat()
    modelo = mostrar_sidebar()
    obtener_mensajes_previos()

    mensaje_usuario = obtener_mensajes_usuario()
    if mensaje_usuario:
        agregar_mensaje("user", mensaje_usuario)
        mostrar_mensaje("user", mensaje_usuario)

        respuesta = cliente.chat.completions.create(
            model=modelo,
            messages=st.session_state.mensajes
        )

        contenido_asistente = respuesta.choices[0].message.content
        agregar_mensaje("assistant", contenido_asistente)
        mostrar_mensaje("assistant", contenido_asistente)

if __name__ == "__main__":
    ejecutar_chat()