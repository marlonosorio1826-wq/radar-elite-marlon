import streamlit as st
import requests
import re
from datetime import date, datetime, timedelta

# --- 1. CONFIGURACIÓN PROFESIONAL Y ESTILO ---
st.set_page_config(page_title="Marlon Pro Elite", layout="wide")

hide_style = """
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;} .stDeployButton {display:none;}
    .stButton > button {
        width: 100% !important; height: 65px !important; background-color: #000000 !important;
        color: #ffffff !important; border: 2px solid #38bdf8 !important; border-radius: 15px !important;
        font-size: 18px !important; font-weight: bold !important;
    }
    .stat-card { background-color: #1e293b; padding: 12px; border-radius: 8px; text-align: center; border-bottom: 4px solid #38bdf8; }
    .goal-card { background-color: #0f172a; padding: 10px; border-radius: 8px; text-align: center; border-bottom: 3px solid #facc15; }
    </style>
    """
st.markdown(hide_style, unsafe_allow_html=True)

# --- 2. ENCABEZADO ---
st.markdown("""
    <div style="text-align: center; padding: 25px; background-color: #000000; border-radius: 15px; border: 2px solid #38bdf8; margin-bottom: 20px;">
        <h1 style="color: #ffffff; margin: 0; font-size: 32px;">🛡️ MARLON PRO ELITE</h1>
        <p style="color: #ffffff; font-size: 20px; font-weight: bold; margin-top: 15px;">
            Inteligencia y Análisis Aplicado a lo Deportivo
        </p>
        <div style="height: 3px; background: linear-gradient(90deg, #38bdf8, #facc15); width: 60%; margin: 15px auto;"></div>
    </div>
    """, unsafe_allow_html=True)

# --- 3. CONFIGURACIÓN API ---
API_KEY = "C87ba92780ea2434174c3f2969ed76eb" 
HEADERS = {'x-rapidapi-key': API_KEY, 'x-rapidapi-host': "v3.football.api-sports.io"}

LIGAS_TOP = [61, 62, 140, 141, 39, 41, 94, 95, 78, 79, 203, 204, 144, 145, 88, 89, 207, 208, 2, 3, 848, 5]

def obtener_datos(endpoint, params=None):
    try:
        url = f"https://v3.football.api-sports.io/{endpoint}"
        res = requests.get(url, headers=HEADERS, params=params).json()
        return res.get('response', [])
    except: return []

def ajustar_hora_francia(fecha_str):
    dt_utc = datetime.fromisoformat(fecha_str.replace('Z', '+00:00'))
    dt_local = dt_utc + timedelta(hours=1) 
    return dt_local.strftime('%H:%M')

# --- 4. SELECTOR DE RADAR ---
if 'seleccion' not in st.session_state: st.session_state.seleccion = "PRÓXIMOS"

col_v, col_p = st.columns(2)
with col_v: 
    if st.button("🚀 EN VIVO"): st.session_state.seleccion = "VIVO"
with col_p: 
    if st.button("📅 PRÓXIMOS"): st.session_state.seleccion = "PRÓXIMOS"

# --- 5. FUNCIÓN DE ANÁLISIS MAESTRO ---
def mostrar_analisis_partido(p, es_vivo=False):
    hora_local = ajustar_hora_francia(p['fixture']['date'])
    status = f"{p['fixture']['status']['elapsed']}'" if es_vivo else hora_local
    
    with st.expander(f"🏟️ {status} | {p['teams']['home']['name']} vs {p['teams']['away']['name']}"):
        if st.button(f"Análisis IA Profundo", key=f"btn_{p['fixture']['id']}"):
            preds_data = obtener_datos("predictions", {"fixture": p['fixture']['id']})
            odds_data = obtener_datos("odds", {"fixture": p['fixture']['id']})
            
            if preds_data:
                pred = preds_data[0]
                pct = pred['predictions']['percent']
                
                # Obtener cuotas si existen
                o_l, o_e, o_v = "-", "-", "-"
                if odds_data:
                    vals = odds_data[0]['bookmakers'][0]['bets'][0]['values']
                    o_l, o_e, o_v = vals[0]['odd'], vals[1]['odd'], vals[2]['odd']

                # --- BLOQUE 1: GANADOR (PORCENTAJES + CUOTAS) ---
                st.markdown("### 📊 Probabilidades y Cuotas (1X2)")
                c1, c2, c3 = st.columns(3)
                with c1: st.markdown(f"<div class='stat-card'><p style='color:#38bdf8;margin:0;'>Local</p><h2>{pct['home']}</h2><p style='color:#facc15;margin:0;'>Cuota: {o_l}</p></div>", unsafe_allow_html=True)
                with c2: st.markdown(f"<div class='stat-card'><p style='color:#38bdf8;margin:0;'>Empate</p><h2>{pct['draw']}</h2><p style='color:#facc15;margin:0;'>Cuota: {o_e}</p></div>", unsafe_allow_html=True)
                with c3: st.markdown(f"<div class='stat-card'><p style='color:#38bdf8;margin:0;'>Visita</p><h2>{pct['away']}</h2><p style='color:#facc15;margin:0;'>Cuota: {o_v}</p></div>", unsafe_allow_html=True)

                # --- BLOQUE 2: GOLES (6 CASILLAS) ---
                st.markdown("### ⚽ Mercado de Goles Detallado")
                g1, g2, g3 = st.columns(3)
                with g1: st.markdown(f"<div class='goal-card'>Más 1.5<br><h3>🟢 {pct['home']}</h3></div>", unsafe_allow_html=True)
                with g2: st.markdown(f"<div class='goal-card'>Más 2.5<br><h3>🟢 {pred['predictions'].get('under_over','-')}</h3></div>", unsafe_allow_html=True)
                with g3: st.markdown(f"<div class='goal-card'>Ambos Marcan<br><h3>⚽ SÍ</h3></div>", unsafe_allow_html=True)
                
                g4, g5, g6 = st.columns(3)
                with g4: st.markdown(f"<div class='goal-card' style='border-color:#ff4b4b;'>Menos 1.5<br><h3>🔴 {pct['draw']}</h3></div>", unsafe_allow_html=True)
                with g5: st.markdown(f"<div class='goal-card' style='border-color:#ff4b4b;'>Menos 2.5<br><h3>🔴 -</h3></div>", unsafe_allow_html=True)
                with g6: st.markdown(f"<div class='goal-card' style='border-color:#38bdf8;'>Total Goles<br><h3>{pred['predictions'].get('under_over','-')}</h3></div>", unsafe_allow_html=True)

                # --- BLOQUE 3: VERDICTO BIG DATA (DOBLE OPORTUNIDAD) ---
                raw_advice = pred['predictions']['advice']
                traducciones = {"Home win": "Victoria Local", "Away win": "Victoria Visitante", "Double chance": "Doble Oportunidad", "draw or": "empate o"}
                consejo_es = raw_advice
                for eng, esp in traducciones.items(): consejo_es = re.sub(eng, esp, consejo_es, flags=re.IGNORECASE)

                st.markdown(f"""
                    <div style="background-color: #000000; padding: 25px; border-radius: 15px; border: 3px solid #38bdf8; margin-top:15px;">
                        <div style="background-color: #0d1117; padding: 20px; border-radius: 10px; border-left: 10px solid #00ff00;">
                            <p style="color: #38bdf8; font-size: 14px; font-weight: bold; margin-bottom: 5px;">🧠 ANÁLISIS BIG DATA & REDES:</p>
                            <p style="color: white; font-size: 20px; margin-bottom: 10px;">💡 Veredicto IA: <span style="color: #00ff00; font-weight: 900;">{consejo_es.upper()}</span></p>
                            <p style="color: #facc15; font-size: 16px; margin: 0;">🛡️ <b>GUÍA REAL RECOMENDADA:</b> Apuesta en {pred['predictions'].get('under_over','-')} Goles.</p>
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
    if not partidos_finales: partidos_finales = partidos[:15]
    for p in partidos_finales: mostrar_analisis_partido(p, es_vivo=(st.session_state.seleccion == "VIVO"))
