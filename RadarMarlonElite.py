import streamlit as st
import requests
import re
from datetime import date

# --- 1. CONFIGURACIÓN PROFESIONAL ---
st.set_page_config(page_title="Marlon Pro Elite", layout="wide")

hide_style = """
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;} .stDeployButton {display:none;}
    .stButton > button {
        width: 100% !important; height: 65px !important; background-color: #000000 !important;
        color: #ffffff !important; border: 2px solid #38bdf8 !important; border-radius: 15px !important;
        font-size: 18px !important; font-weight: bold !important;
    }
    .stat-card { background-color: #1e293b; padding: 12px; border-radius: 8px; text-align: center; border-bottom: 3px solid #38bdf8; margin-bottom: 10px; }
    .goal-card { background-color: #0f172a; padding: 10px; border-radius: 8px; text-align: center; border-bottom: 3px solid #facc15; margin-bottom: 10px; }
    </style>
    """
st.markdown(hide_style, unsafe_allow_html=True)

# --- 2. ENCABEZADO ---
st.markdown("""
    <div style="text-align: center; padding: 25px; background-color: #000000; border-radius: 15px; border: 2px solid #38bdf8; margin-bottom: 20px;">
        <h1 style="color: #ffffff; margin: 0; font-size: 32px;">🛡️ MARLON PRO ELITE</h1>
        <p style="color: #ffffff; font-size: 20px; font-weight: bold; margin-top: 15px;">Inteligencia y Análisis Aplicado a lo Deportivo</p>
        <div style="height: 3px; background: linear-gradient(90deg, #38bdf8, #facc15); width: 60%; margin: 15px auto;"></div>
    </div>
    """, unsafe_allow_html=True)

# --- 3. CONFIGURACIÓN API Y LIGAS EXTENDIDAS ---
API_KEY = "6e034dd86fa0adda024699350e5f87d2" 
HEADERS = {'x-rapidapi-key': API_KEY, 'x-rapidapi-host': "v3.football.api-sports.io"}

# Lista extendida: Francia, España, Inglaterra, Portugal, Turquía, Alemania (Ligas 1 y 2)
LIGAS_TOP = [
    61, 62,   # Francia
    140, 141, # España
    39, 41,   # Inglaterra
    94, 95,   # Portugal (Primeira y Segunda)
    203, 204, # Turquía (Süper Lig y 1. Lig)
    78, 79    # Alemania (Bundesliga 1 y 2)
]

def obtener_datos(endpoint, params=None):
    try:
        url = f"https://v3.football.api-sports.io/{endpoint}"
        res = requests.get(url, headers=HEADERS, params=params).json()
        return res.get('response', [])
    except: return []

# --- 4. SELECTOR DE RADAR ---
if 'seleccion' not in st.session_state: st.session_state.seleccion = "PRÓXIMOS"

st.markdown("<p style='color: #38bdf8; font-weight: bold; text-align: center; margin-bottom: 10px; font-size: 18px;'>📡 SELECTOR DE RADAR</p>", unsafe_allow_html=True)
col_v, col_p = st.columns(2)
with col_v: 
    if st.button("🚀 EN VIVO"): st.session_state.seleccion = "VIVO"
with col_p: 
    if st.button("📅 PRÓXIMOS"): st.session_state.seleccion = "PRÓXIMOS"

st.markdown(f"<p style='text-align: center; color: #facc15; font-weight: bold;'>MODO ACTUAL: {st.session_state.seleccion}</p>", unsafe_allow_html=True)
st.markdown("---")

# --- 5. FUNCIÓN DE ANÁLISIS MAESTRO ---
def mostrar_analisis_partido(p, es_vivo=False):
    status = f"{p['fixture']['status']['elapsed']}'" if es_vivo else p['fixture']['date'][11:16]
    with st.expander(f"🏟️ {status} | {p['teams']['home']['name']} vs {p['teams']['away']['name']}"):
        if st.checkbox("🔍 Cargar Análisis Profundo", key=f"check_{p['fixture']['id']}"):
            preds_data = obtener_datos("predictions", {"fixture": p['fixture']['id']})
            if preds_data:
                pred = preds_data[0]
                pct = pred['predictions']['percent']
                
                # --- BLOQUE 1: PROBABILIDADES GANADOR (3 CASILLAS) ---
                st.markdown("### 📊 Probabilidades 1X2 (%)")
                c1, c2, c3 = st.columns(3)
                with c1: st.markdown(f"<div class='stat-card'><p style='color:#38bdf8;margin:0;'>Local</p><h2>{pct['home']}</h2></div>", unsafe_allow_html=True)
                with c2: st.markdown(f"<div class='stat-card'><p style='color:#38bdf8;margin:0;'>Empate</p><h2>{pct['draw']}</h2></div>", unsafe_allow_html=True)
                with c3: st.markdown(f"<div class='stat-card'><p style='color:#38bdf8;margin:0;'>Visita</p><h2>{pct['away']}</h2></div>", unsafe_allow_html=True)

                # --- BLOQUE 2: ANÁLISIS DE GOLES (6 CASILLAS) ---
                st.markdown("### ⚽ Mercado de Goles (Over / Under)")
                g1, g2, g3 = st.columns(3)
                with g1: st.markdown(f"<div class='goal-card'>Más 1.5<br><h3>🟢 {pct['home']}</h3></div>", unsafe_allow_html=True)
                with g2: st.markdown(f"<div class='goal-card'>Más 2.5<br><h3>🟢 {pred['predictions']['under_over']}</h3></div>", unsafe_allow_html=True)
                with g3: st.markdown(f"<div class='goal-card'>Ambos Marcan<br><h3>⚽ SÍ</h3></div>", unsafe_allow_html=True)
                
                g4, g5, g6 = st.columns(3)
                with g4: st.markdown(f"<div class='goal-card' style='border-color:#ff4b4b;'>Menos 1.5<br><h3>🔴 {pct['draw']}</h3></div>", unsafe_allow_html=True)
                with g5: st.markdown(f"<div class='goal-card' style='border-color:#ff4b4b;'>Menos 2.5<br><h3>🔴 -</h3></div>", unsafe_allow_html=True)
                with g6: st.markdown(f"<div class='goal-card' style='border-color:#38bdf8;'>Total Prob.<br><h3>{pred['predictions']['under_over']}</h3></div>", unsafe_allow_html=True)

                # --- BLOQUE 3: EL VERDICTO MAESTRO (BIG DATA) ---
                raw_advice = pred['predictions']['advice']
                traducciones = {"Home win": "Victoria Local", "Away win": "Victoria Visitante", "Double chance": "Doble Oportunidad", "draw or": "empate o"}
                consejo_es = raw_advice
                for eng, esp in traducciones.items(): consejo_es = re.sub(eng, esp, consejo_es, flags=re.IGNORECASE)

                st.markdown(f"""
                    <div style="background-color: #000000; padding: 25px; border-radius: 15px; border: 3px solid #38bdf8; margin-top:20px;">
                        <div style="background-color: #0d1117; padding: 20px; border-radius: 10px; border-left: 10px solid #00ff00;">
                            <p style="color: #38bdf8; font-size: 14px; font-weight: bold; margin-bottom: 5px;">🧠 ANÁLISIS BIG DATA & REDES:</p>
                            <p style="color: white; font-size: 20px; margin-bottom: 10px;">💡 Veredicto IA: <span style="color: #00ff00; font-weight: 900;">{consejo_es.upper()}</span></p>
                            <p style="color: #facc15; font-size: 16px; margin: 0;">🛡️ <b>GUÍA RECOMENDADA:</b> {pred['predictions']['under_over']} goles.</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

# --- 6. EJECUCIÓN ---
if st.session_state.seleccion == "VIVO":
    partidos = obtener_datos("fixtures", {"live": "all"})
else:
    hoy = date.today().strftime('%Y-%m-%d')
    partidos = obtener_datos("fixtures", {"date": hoy})

if partidos:
    partidos_finales = [p for p in partidos if p['league']['id'] in LIGAS_TOP]
    
    # Si no hay partidos en las ligas top hoy, muestra los más importantes del día
    if not partidos_finales:
        partidos_finales = partidos[:15]
        st.warning("Sin partidos en tus ligas principales. Analizando otros destacados:")
        
    for p in partidos_finales:
        mostrar_analisis_partido(p, es_vivo=(st.session_state.seleccion == "VIVO"))
else:
    st.info("No se encontraron partidos para analizar.")
