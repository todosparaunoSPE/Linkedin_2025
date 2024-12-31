# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 11:46:30 2024

@author: jperezr
"""

import streamlit as st
import time
import datetime
import random
import pandas as pd
import requests
import json
import base64
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(page_title="Feliz Año 2025", page_icon="🎉")

# Estilo de fondo
page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
background:
radial-gradient(black 15%, transparent 16%) 0 0,
radial-gradient(black 15%, transparent 16%) 8px 8px,
radial-gradient(rgba(255,255,255,.1) 15%, transparent 20%) 0 1px,
radial-gradient(rgba(255,255,255,.1) 15%, transparent 20%) 8px 9px;
background-color:#282828;
background-size:16px 16px;
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# Título inicial
st.title("🎉 ¡Bienvenidos! 🎉")

# Texto que se mostrará letra por letra
mensaje = "🎉 Feliz Año 2025 🎉"

# Contenedor para las letras
espacio = st.empty()

# Mostrar las letras una por una
texto_mostrado = ""
for letra in mensaje:
    texto_mostrado += letra
    espacio.markdown(f"<h1 style='text-align: center; color: #ff4500;'>{texto_mostrado}</h1>", unsafe_allow_html=True)
    time.sleep(0.3)  # Tiempo de retraso en segundos

# Mensaje con efecto de parpadeo para contactos de Linkedin
st.write("---")  # Separador
st.markdown(
    """
    <style>
    .blink {
        text-align: center;
        color: #007bff;
        font-size: 24px;
        animation: blink-animation 1s steps(2, start) infinite;
    }
    @keyframes blink-animation {
        to {
            visibility: hidden;
        }
    }
    </style>
    <div class="blink">🎊 ¡Un saludo especial para todos aquellos que utilizan LinkedIn! 🎊</div>
    """,
    unsafe_allow_html=True
)

# Confeti animado
confetti_html = """
<script>
(function() {
    const confetti = document.createElement('script');
    confetti.src = 'https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js';
    confetti.onload = () => {
        const duration = 5 * 1000;
        const end = Date.now() + duration;
        (function frame() {
            confetti({
                particleCount: 5,
                angle: 60,
                spread: 55,
                origin: { x: 0 }
            });
            confetti({
                particleCount: 5,
                angle: 120,
                spread: 55,
                origin: { x: 1 }
            });
            if (Date.now() < end) {
                requestAnimationFrame(frame);
            }
        })();
    };
    document.head.appendChild(confetti);
})();
</script>
"""
components.html(confetti_html)

# Reemplaza con tus credenciales de GitHub y el nombre del repositorio
GITHUB_API_URL = "https://github.com/todosparaunoSPE/Linkedin_2025/blob/main/deseos.csv"
GITHUB_TOKEN = "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"

# Función para obtener el contenido del archivo desde GitHub
def obtener_contenido_github():
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(GITHUB_API_URL, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"No se pudo obtener el archivo. Error {response.status_code}")
        return None

# Función para actualizar el archivo en GitHub
def actualizar_archivo_github(nuevo_deseo):
    contenido = obtener_contenido_github()
    
    if contenido is not None:
        # Obtener el contenido del archivo codificado en base64
        archivo_base64 = contenido['content']
        archivo_decodificado = base64.b64decode(archivo_base64).decode('utf-8')

        # Convertir a DataFrame y agregar el nuevo deseo
        df = pd.read_csv(pd.compat.StringIO(archivo_decodificado))
        df = df.append({"Deseo": nuevo_deseo}, ignore_index=True)

        # Codificar el DataFrame actualizado en base64
        archivo_actualizado = df.to_csv(index=False)
        archivo_base64_actualizado = base64.b64encode(archivo_actualizado.encode('utf-8')).decode('utf-8')

        # Crear el payload para la API de GitHub
        payload = {
            "message": f"Agregar nuevo deseo: {nuevo_deseo}",
            "content": archivo_base64_actualizado,
            "sha": contenido['sha']
        }

        # Realizar la solicitud PUT para actualizar el archivo
        headers = {'Authorization': f'token {GITHUB_TOKEN}'}
        response = requests.put(GITHUB_API_URL, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            st.success("¡Deseo guardado exitosamente!")
        else:
            st.error(f"No se pudo guardar el deseo. Error {response.status_code}")

# Formulario para enviar deseos
deseo = st.text_input("Escribe tus buenos deseos para todos los que utilizan LinkedIn", key="deseos")
if st.button("Enviar deseo"):
    if deseo.strip():
        actualizar_archivo_github(deseo.strip())
        st.success(f"🎉 ¡Gracias por compartir tu deseo: {deseo}! ")
    else:
        st.warning("Por favor, escribe un deseo antes de enviarlo.")

# Mensajes aleatorios de buenos deseos
mensajes = [
    "¡Que este año te traiga mucha felicidad y éxito! 🎉",
    "¡Que todos tus sueños se hagan realidad en 2025! 🌟",
    "¡Disfruta cada momento de este nuevo año! 🌈",
]

mensaje_random = random.choice(mensajes)
st.info(f"💬 {mensaje_random}")

# Barra lateral con cuenta regresiva
with st.sidebar:
    st.header("⏳ Cuenta Regresiva para el Año Nuevo 2025 ⏳")

    # Mostrar tu nombre
    st.write("👤 **Javier Horacio Pérez Ricárdez**")
    
    # Insertar emojis para mayor interactividad
    st.markdown("🎉 **¡Falta poco para el Año Nuevo!** 🎉")
    st.image("https://www.w3schools.com/w3images/lights.jpg", caption="¡El Año Nuevo está por llegar!", use_container_width=True)

    # Reloj de cuenta regresiva dinámica con segundos
    año_nuevo = datetime.datetime(2025, 1, 1, 0, 0, 0)
    espacio_contador = st.empty()  # Contenedor para la cuenta regresiva

    while True:
        ahora = datetime.datetime.now() - datetime.timedelta(hours=6)  # Restar las 9 horas de desfase
        tiempo_restante = año_nuevo - ahora

        # Mostrar la cuenta regresiva con días, horas, minutos y segundos
        espacio_contador.markdown(f"""
        <h2 style="text-align:center; color: #ff4500;">
        ⏳ Tiempo restante para 2025: {tiempo_restante.days} días, {tiempo_restante.seconds // 3600} horas, 
        {(tiempo_restante.seconds // 60) % 60} minutos, {tiempo_restante.seconds % 60} segundos.
        </h2>
        """, unsafe_allow_html=True)

        # Actualizar cada segundo
        time.sleep(1)

# Fondo animado
st.markdown(
    """
    <style>
    body {
        background: radial-gradient(circle, #ffe4e1, #ff4500, #ff6347);
        animation: background-animation 5s infinite;
    }
    @keyframes background-animation {
        0% {background: #ffe4e1;}
        50% {background: #ff4500;}
        100% {background: #ff6347;}
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Mensaje final
st.success(" ¡Que sea un año lleno de éxitos y felicidad para todos!")
