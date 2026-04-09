import streamlit as st
from groq import Groq
import pandas as pd
import os
from datetime import datetime
from collections import Counter

# --- CONFIGURACIÓN ---
API_KEY = "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"
client = Groq(api_key=API_KEY)
ARCHIVO_HISTORIAL = "historial.csv"

# Verificación y autoreparación del CSV
if not os.path.exists(ARCHIVO_HISTORIAL):
    df_inicial = pd.DataFrame(columns=["Fecha", "Busqueda", "Recomendaciones", "Voto", "Vistas"])
    df_inicial.to_csv(ARCHIVO_HISTORIAL, index=False)
else:
    df_check = pd.read_csv(ARCHIVO_HISTORIAL)
    if 'Vistas' not in df_check.columns:
        df_check['Vistas'] = "Ninguna"
        df_check.to_csv(ARCHIVO_HISTORIAL, index=False)

# --- MEMORIA (Session State) ---
if "respuesta_ia" not in st.session_state:
    st.session_state.respuesta_ia = None
if "busqueda_actual" not in st.session_state:
    st.session_state.busqueda_actual = ""
if "confirmar_borrado" not in st.session_state:
    st.session_state.confirmar_borrado = False

# --- ENCABEZADO ---
col_izq, col_logo, col_der = st.columns([1, 0.8, 1]) 

with col_logo:
    try:
        if os.path.exists("IconoMoviMindAIBueno.png"):
            st.image("IconoMoviMindAIBueno.png", use_container_width=True)
        else:
            st.markdown("<h1 style='text-align: center;'>🎬</h1>", unsafe_allow_html=True)
    except:
        st.markdown("<h1 style='text-align: center;'>🎬</h1>", unsafe_allow_html=True)

# Títulos principales
st.markdown("<h1 style='text-align: center;' class='cinema-title'>MovieMind IA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; opacity: 0.8; font-style: italic;'>Tu crítico personal de cine</p>", unsafe_allow_html=True)

# --- INTERFAZ ---
st.set_page_config(page_title="MovieMind IA", page_icon="🎬", layout="centered")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; background-color: #E50914; color: white !important; font-weight: bold; }
    .cinema-title { color: #D4AF37; text-align: center; font-weight: 800; }
    .stTextInput>div>div>input { border: 2px solid #D4AF37; }
    .stat-card { background-color: rgba(212, 175, 55, 0.1); padding: 15px; border-radius: 10px; border: 1px solid #D4AF37; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE DATOS (HISTORIAL Y VISTAS) ---
contexto_historial = ""
peliculas_vistas_str = "Ninguna"

if os.path.exists(ARCHIVO_HISTORIAL):
    df_h = pd.read_csv(ARCHIVO_HISTORIAL)
    if not df_h.empty:
        # Contexto de gustos
        ultimos_votos = df_h.tail(5)
        for _, fila in ultimos_votos.iterrows():
            contexto_historial += f"- Buscó: {fila['Busqueda']} | Voto: {fila['Voto']}\n"
        
        # Filtro de películas prohibidas
        if 'Vistas' in df_h.columns:
            todas = df_h['Vistas'].str.split(', ').explode()
            lista_vistas = todas[(todas != "Ninguna") & (todas.notna()) & (todas != "")].unique().tolist()
            if lista_vistas:
                peliculas_vistas_str = ", ".join(lista_vistas)

# --- ENTRADA DE USUARIO ---
user_query = st.text_input("🍿 ¿Qué quieres ver hoy?", placeholder="Ej: Ciencia ficción tipo Interstellar...")

if st.button("GENERAR RECOMENDACIONES 🎬", key="btn_principal"):
    if user_query:
        try:
            with st.spinner('🎞️ Consultando archivos de Hollywood...'):
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system", 
                            # AQUÍ ES DONDE PEGAS EL CONTENIDO NUEVO:
                            "content": f"""Eres un experto cinéfilo de élite.
HISTORIAL: {contexto_historial}
⚠️ PROHIBICIÓN: No recomiendes bajo ningún concepto estas películas: {peliculas_vistas_str}

REGLAS ESTRICTAS DE FORMATO:
Para cada película usa exactamente este orden y estos iconos para que mi sistema pueda leerlos:
• **Título**
🎭 **Género:** [Género]
⭐ **IMDb:** [Nota]/10
📝 **Sinopsis:** [Descripción corta]"""
                        },
                        {"role": "user", "content": user_query}
                    ],
                    model="llama-3.3-70b-versatile",
                )
                st.session_state.respuesta_ia = chat_completion.choices[0].message.content
                st.session_state.busqueda_actual = user_query
                st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

# --- RESULTADOS Y VOTACIÓN (DISEÑO PREMIUM EN COLUMNAS) ---
if st.session_state.respuesta_ia:
    st.markdown("### 🍿 Selección de la Crítica")
    
    import re
    # Buscamos bloques que empiecen por el título en negritas y capturen el resto
    bloques = re.split(r"\n(?=[•\-\*]\s*\*\*)", st.session_state.respuesta_ia.strip())
    
    # Limpiamos bloques vacíos
    bloques = [b for b in bloques if "**" in b]

    # --- CAMBIO AQUÍ: Inicializamos la lista para evitar el error de NameError ---
    vistas_ahora = [] 

    # Crear 3 columnas para las tarjetas de películas
    cols_cards = st.columns(3)
    titulos_deteccion = []

    for i, bloque in enumerate(bloques[:3]):
        with cols_cards[i]:
            # Extraer Título, Género, IMDb y Sinopsis del bloque de texto
            titulo = re.search(r"\*\*(.*?)\*\*", bloque)
            genero = re.search(r"🎭 \*\*Género:\*\* (.*)", bloque)
            nota = re.search(r"⭐ \*\*IMDb:\*\* (.*)", bloque)
            sinopsis = re.search(r"📝 \*\*Sinopsis:\*\* (.*)", bloque)

            titulo_txt = titulo.group(1) if titulo else f"Película {i+1}"
            titulos_deteccion.append(titulo_txt)

            # Tarjeta visual con HTML/CSS (He añadido una altura fija de 280px para que queden simétricas)
            st.markdown(f"""
                <div style="
                    border: 2px solid #D4AF37;
                    border-radius: 15px;
                    padding: 15px;
                    height: 280px;
                    background-color: rgba(212, 175, 55, 0.05);
                    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
                    overflow: hidden;
                ">
                    <h4 style="color: #D4AF37; margin-bottom: 10px; text-align: center; font-size: 1.1em;">{titulo_txt}</h4>
                    <p style="font-size: 0.85em; margin-bottom: 5px;">🎭 <b>Género:</b> {genero.group(1) if genero else 'N/A'}</p>
                    <p style="font-size: 0.85em; margin-bottom: 5px;">⭐ <b>IMDb:</b> {nota.group(1) if nota else 'N/A'}</p>
                    <hr style="margin: 10px 0; border: 0.5px solid rgba(212, 175, 55, 0.3);">
                    <p style="font-size: 0.8em; font-style: italic; line-height: 1.4;">{sinopsis.group(1) if sinopsis else 'Sin descripción disponible.'}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # El checkbox ahora ya sabe dónde guardar los datos
            if st.checkbox(f"La veré", key=f"chk_{i}_{titulo_txt[:5]}"):
                vistas_ahora.append(titulo_txt)

    st.write("---")
    
    # SECCIÓN DE VOTACIÓN
    st.markdown("<h4 style='text-align: center; color: #D4AF37;'>⭐ Califica esta recomendación ⭐</h4>", unsafe_allow_html=True)
    st.markdown("""<style>.stFeedbackContainer { transform: scale(2.5) !important; margin: 40px 0 !important; justify-content: center !important; }</style>""", unsafe_allow_html=True)
    rating = st.feedback("stars")
    
    if rating is not None:
        puntuacion = rating + 1
        if st.button("Confirmar Voto", width='stretch', key="save_vote"):
            texto_vistas = ", ".join(vistas_ahora) if vistas_ahora else "Ninguna"
            nueva_fila = {
                "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Busqueda": st.session_state.busqueda_actual,
                "Recomendaciones": ", ".join(titulos_deteccion),
                "Voto": f"{puntuacion} ⭐",
                "Vistas": texto_vistas
            }
            df = pd.read_csv(ARCHIVO_HISTORIAL)
            df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
            df.to_csv(ARCHIVO_HISTORIAL, index=False)
            st.toast("🎬 ¡Preferencias guardadas!")
            st.rerun()

# --- BIBLIOTECA DE VISTAS ---
st.write("---")
st.markdown("<h3 style='text-align: center; color: #D4AF37;'>🎬 Mi Biblioteca</h3>", unsafe_allow_html=True)
if os.path.exists(ARCHIVO_HISTORIAL):
    df_v = pd.read_csv(ARCHIVO_HISTORIAL)
    if 'Vistas' in df_v.columns:
        vistas_all = df_v['Vistas'].str.split(', ').explode()
        lista_p = vistas_all[(vistas_all != "Ninguna") & (vistas_all.notna()) & (vistas_all != "")].unique()
        if len(lista_p) > 0:
            c_vistas = st.columns(4)
            for i, peli in enumerate(sorted(lista_p)):
                with c_vistas[i % 4]:
                    st.markdown(f"<div style='background:rgba(212,175,55,0.1); border:1px solid #D4AF37; padding:10px; border-radius:10px; text-align:center; margin-bottom:10px; font-size:0.8em;'>🎥 {peli}</div>", unsafe_allow_html=True)

# --- HISTORIAL COMPLETO ---
st.write("---")
with st.expander("📜 Historial de Búsquedas"):
    if os.path.exists(ARCHIVO_HISTORIAL):
        df_hist = pd.read_csv(ARCHIVO_HISTORIAL)
        st.dataframe(df_hist[::-1], use_container_width=True, hide_index=True)