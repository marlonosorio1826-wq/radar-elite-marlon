
import streamlit as st
import requests
import re
from datetime import date

# --- 1. CONFIGURACIÓN PROFESIONAL (CERO RASTRO DE STREAMLIT) ---
st.set_page_config(page_title="Marlon Pro Elite", layout="wide")

hide_style = """
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;} .stDeployButton {display:none;}
    
    /* Botones de Navegación */
    .stButton > button {
        width: 100% !important; height: 65px !important; background-color: #000000 !important;
        color: #ffffff !important; border: 2px solid #38bdf8 !important; border-radius: 15px !important;
        font-size: 18px !important; font-weight: bold !important; transition: 0.3s;
    }
    .stButton > button:hover { border-color: #facc15 !important; color: #facc15 !important; box-shadow: 0px 0px 15px #38bdf8; }
    
    /* Tarjetas de Datos */
    .stat-card { background-color: #1e293b; padding: 12px; border-radius: 8px; text-align: center; border-bottom: 3px solid #38bdf8; margin-bottom: 10px; }
    .goal-card { background-color: #0f172a; padding: 10px; border-radius: 8px; text-align: center; border-bottom: 3px solid #facc15; margin-bottom: 10px; }
    </style>
    """
st.markdown(hide_style, unsafe_allow_html=True)

# --- 2. ENCABEZADO PERSONALIZADO ---
st.markdown("""
    <div style="text-align: center; padding: 25px; background-color: #000000; border-radius: 15px; border: 2px solid #38bdf8; margin-bottom: 20px;">
        <h1 style="color: #ffffff; margin: 0; font-size: 32px;">🛡️ MARLON PRO ELITE</h1>
        <p style="color: #ffffff; font-size: 20px; font-weight: bold; margin-top: 15px;">
            Inteligencia y Análisis Aplicado a lo Deportivo
        </p>
        <div style="height: 3px; background: linear-gradient(90deg, #38bdf8, #facc15); width: 60%; margin: 15px auto;"></div>
    </div>
    """, unsafe_allow_html=True)

# --- 3. CONFIGURACIÓN API (VERIFICAR TU KEY) ---
API_KEY = "b7f271a62e0844b1ac5b1e19638dff75" 
HEADERS = {'x-rapidapi-key': API_KEY, 'x-rapidapi-host': "v3.football.api-sports.io"}
LIGAS = [61, 62, 140, 141, 39, 41, 135, 136, 78, 79, 2, 3]

def obtener_datos(endpoint, params=None):
    try:
        url = f"https://v3.football.api-sports.io/{endpoint}"
        res = requests.get(url, headers=HEADERS, params=params).json()
        return res.get('response', [])
    except: return []

# --- 4. SELECTOR DE RADAR (CENTRAL) ---
if 'seleccion' not in st.session_state: st.session_state.seleccion = "PRÓXIMOS"

st.markdown("<p style='color: #38bdf8; font-weight: bold; text-align: center; margin-bottom: 10px; font-size: 18px;'>📡 SELECTOR DE RADAR</p>", unsafe_allow_html=True)
col_v, col_p = st.columns(2)
with col_v: 
    if st.button("🚀 EN VIVO"): st.session_state.seleccion = "VIVO"
with col_p: 
    if st.button("📅 PRÓXIMOS"): st.session_state.seleccion = "PRÓXIMOS"

st.markdown(f"<p style='text-align: center; color: #facc15; font-weight: bold;'>MODO: {st.session_state.seleccion}</p>", unsafe_allow_html=True)

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
                with c1: st.markdown(f"<div class='stat-card'><p style='color:#38bdf8;margin:0;font-size:14px;'>Local</p><h2 style='margin:0;'>{pct['home']}</h2></div>", unsafe_allow_html=True)
                with c2: st.markdown(f"<div class='stat-card'><p style='color:#38bdf8;margin:0;font-size:14px;'>Empate</p><h2 style='margin:0;'>{pct['draw']}</h2></div>", unsafe_allow_html=True)
                with c3: st.markdown(f"<div class='stat-card'><p style='color:#38bdf8;margin:0;font-size:14px;'>Visita</p><h2 style='margin:0;'>{pct['away']}</h2></div>", unsafe_allow_html=True)

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

                # --- BLOQUE 3: VERDICTO DE LA GUÍA (BIG DATA) ---
                raw_advice = pred['predictions']['advice']
                traducciones = {"Home win": "Victoria Local", "Away win": "Victoria Visitante", "Double chance": "Doble Oportunidad", "draw or": "empate o"}
                consejo_es = raw_advice
                for eng, esp in traducciones.items(): consejo_es = re.sub(eng, esp, consejo_es, flags=re.IGNORECASE)

                # Lógica de Recomendación
                confianza = "ALTA" if int(pct['home'].replace('%','')) > 60 or int(pct['away'].replace('%','')) > 60 else "MEDIA"
                apuesta = "Doble Oportunidad + Goles" if "Doble" in consejo_es else "Ganador Directo"

                st.markdown(f"""
                    <div style="background-color: #000000; padding: 25px; border-radius: 15px; border: 3px solid #38bdf8; margin-top:15px;">
                        <div style="background-color: #0d1117; padding: 20px; border-radius: 10px; border-left: 10px solid #00ff00;">
                            <p style="color: #38bdf8; font-size: 14px; font-weight: bold; margin-bottom: 5px;">🧠 ANÁLISIS BIG DATA & REDES:</p>
                            <p style="color: white; font-size: 20px; margin-bottom: 10px;">
                                💡 Veredicto IA: <span style="color: #00ff00; font-weight: 900;">{consejo_es.upper()}</span>
                            </p>
                            <p style="color: #facc15; font-size: 16px; margin: 0;">
                                🛡️ <b>TIPO DE APUESTA RECOMENDADA:</b> {apuesta} <br>
                                📈 <b>NIVEL DE CONFIANZA:</b> {confianza} <br>
                                🎯 <b>GUÍA TÉCNICA:</b> Expectativa de {pred['predictions']['under_over']} goles.
                            </p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                # --- BLOQUE 4: CUOTAS ---
                odds_data = obtener_datos("odds", {"fixture": p['fixture']['id']})
                if odds_data:
                    st.markdown("### 💵 Cuotas en Tiempo Real")
                    o = odds_data[0]['bookmakers'][0]['bets'][0]['values']
                    st.info(f"🏠 Local: **{o[0]['odd']}** | 🤝 Empate: **{o[1]['odd']}** | 🚀 Visita: **{o[2]['odd']}**")

# --- 6. EJECUCIÓN DEL RADAR ---
if st.session_state.seleccion == "VIVO":
    partidos = obtener_datos("fixtures", {"live": "all"})
    for p in [x for x in partidos if x['league']['id'] in LIGAS]: mostrar_analisis_partido(p, es_vivo=True)
else:
    hoy = date.today().strftime('%Y-%m-%d')
    partidos = obtener_datos("fixtures", {"date": hoy})
    for p in [x for x in partidos if x['league']['id'] in LIGAS]: mostrar_analisis_partido(p, es_vivo=False)
