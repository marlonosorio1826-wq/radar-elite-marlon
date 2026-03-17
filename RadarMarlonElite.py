import streamlit as st
import requests
import re
from datetime import date

# --- 1. CONFIGURACIÓN PROFESIONAL ---
st.set_page_config(page_title="Marlon Pro Elite", layout="wide")

# Ocultar rastro de Streamlit
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Estilo para que el selector se vea grande en móvil */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #000000 !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 10px !important;
    }
    .stSelectbox label {
        color: #38bdf8 !important;
        font-weight: bold !important;
        font-size: 18px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ENCABEZADO PERSONALIZADO ---
st.markdown("""
    <div style="text-align: center; padding: 25px; background-color: #000000; border-radius: 15px; border: 2px solid #38bdf8; margin-bottom: 20px;">
        <h1 style="color: #ffffff; margin: 0; font-size: 32px; font-family: sans-serif;">🛡️ MARLON PRO ELITE</h1>
        <p style="color: #ffffff; font-size: 20px; font-weight: bold; margin-top: 15px;">
            Inteligencia y Análisis Aplicado a lo Deportivo
        </p>
        <div style="height: 3px; background: linear-gradient(90deg, #38bdf8, #facc15); width: 60%; margin: 15px auto;"></div>
    </div>
    """, unsafe_allow_html=True)

# --- 3. CONFIGURACIÓN DE API Y LIGAS ---
# Reemplaza con tu clave real
API_KEY = "b7f271a62e0844b1ac5b1e19638dff75" 
HEADERS = {'x-rapidapi-key': API_KEY, 'x-rapidapi-host': "v3.football.api-sports.io"}
LIGAS = [61, 62, 140, 141, 39, 41, 135, 136, 78, 79, 2, 3]

def obtener_datos(endpoint, params=None):
    try:
        url = f"https://v3.football.api-sports.io/{endpoint}"
        res = requests.get(url, headers=HEADERS, params=params).json()
        return res.get('response', [])
    except:
        return []

# --- 4. SELECTOR DE RADAR (ESTILO CLÁSICO GARANTIZADO) ---
opcion = st.selectbox(
    "📡 SELECTOR DE RADAR:",
    ["📊 PRÓXIMOS (Pre-Match)", "🚀 EN VIVO (Live Analysis)"]
)

st.markdown("---")

# --- 5. FUNCIÓN DE ANÁLISIS DETALLADO ---
def mostrar_analisis_partido(p, es_vivo=False):
    status = f"{p['fixture']['status']['elapsed']}'" if es_vivo else p['fixture']['date'][11:16]
    label_vivo = "🔴 EN VIVO" if es_vivo else "📅"
    
    with st.expander(f"{label_vivo} {status} | {p['teams']['home']['name']} vs {p['teams']['away']['name']}"):
        if st.checkbox("🔍 Cargar Análisis Profundo", key=f"check_{p['fixture']['id']}"):
            tab1, tab2 = st.tabs(["🎯 Panel Consejos IA", "📊 H2H"])
            
            with tab1:
                preds_data = obtener_datos("predictions", {"fixture": p['fixture']['id']})
                if preds_data:
                    pred = preds_data[0]
                    # Traducción agresiva al español
                    raw_advice = pred['predictions']['advice']
                    traducciones = {
                        "Home win": "Victoria Local", "Away win": "Victoria Visitante", 
                        "Draw": "Empate", "Double chance": "Doble Oportunidad",
                        "draw or": "empate o", "or": "o", "and": "y"
                    }
                    consejo_es = raw_advice
                    for eng, esp in traducciones.items():
                        consejo_es = re.sub(eng, esp, consejo_es, flags=re.IGNORECASE)

                    # Estilo de alto contraste pedido
                    st.markdown(f"""
                        <div style="background-color: #000000; padding: 25px; border-radius: 15px; border: 3px solid #38bdf8;">
                            <p style="color: white; font-size: 20px;">👑 <b>Probabilidades:</b><br>
                            <span style="color: #facc15; font-size: 22px; font-weight: bold;">
                                {pred['predictions']['percent']['home']} Local | {pred['predictions']['percent']['away']} Visita
                            </span></p>
                            <div style="background-color: #1a1a1a; padding: 15px; border-radius: 10px; border-left: 8px solid #00ff00; margin-top: 15px;">
                                <p style="color: white; font-size: 18px; margin: 0;">💡 <b>VERDICTO FINAL IA:</b><br>
                                <span style="color: #00ff00; font-weight: 900; font-size: 22px; text-transform: uppercase;">{consejo_es}</span></p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            
            with tab2:
                st.write("Cargando historial de enfrentamientos directos...")

# --- 6. LÓGICA DE CARGA ---
if "EN VIVO" in opcion:
    partidos = obtener_datos("fixtures", {"live": "all"})
    if partidos:
        for p in [x for x in partidos if x['league']['id'] in LIGAS]:
            mostrar_analisis_partido(p, es_vivo=True)
    else:
        st.info("No hay partidos en vivo en las ligas seleccionadas.")
else:
    hoy = date.today().strftime('%Y-%m-%d')
    partidos = obtener_datos("fixtures", {"date": hoy})
    for p in [x for x in partidos if x['league']['id'] in LIGAS]:
        mostrar_analisis_partido(p, es_vivo=False)
