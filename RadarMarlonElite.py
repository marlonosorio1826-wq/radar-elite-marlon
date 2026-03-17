import streamlit as st
import requests
import re
from datetime import date

# --- 1. CONFIGURACIÓN DE APARIENCIA PROFESIONAL (SIN RASTRO DE STREAMLIT) ---
st.set_page_config(page_title="Marlon Pro Elite", layout="wide")

hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Botones de navegación (Pills) estilo App de Élite */
    [data-testid="stBaseButton-pill"] {
        width: 100% !important;
        height: 60px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border: 2px solid #38bdf8 !important;
        background-color: #000000 !important;
        color: white !important;
        margin-bottom: 15px !important;
        border-radius: 12px !important;
    }
    [data-testid="stBaseButton-pillActive"] {
        background-color: #38bdf8 !important;
        color: #000000 !important;
        box-shadow: 0px 0px 15px #38bdf8;
    }
    </style>
    """
st.markdown(hide_style, unsafe_allow_html=True)

# --- 2. ENCABEZADO PERSONALIZADO ---
st.markdown("""
    <div style="text-align: center; padding: 25px; background-color: #000000; border-radius: 15px; border: 2px solid #38bdf8; margin-bottom: 30px;">
        <h1 style="color: #ffffff; margin: 0; font-size: 32px; font-family: sans-serif;">🛡️ MARLON PRO ELITE</h1>
        <p style="color: #ffffff; font-size: 20px; font-weight: bold; margin-top: 15px;">
            Inteligencia y Análisis Aplicado a lo Deportivo
        </p>
        <div style="height: 3px; background: linear-gradient(90deg, #38bdf8, #facc15); width: 60%; margin: 15px auto;"></div>
    </div>
    """, unsafe_allow_html=True)

# --- 3. CONFIGURACIÓN DE DATOS Y API ---
API_KEY = "b7f271a62e0844b1ac5b1e19638dff75" 
HEADERS = {'x-rapidapi-key': API_KEY, 'x-rapidapi-host': "v3.football.api-sports.io"}

# Lista de ligas que analizamos (Francia, España, Inglaterra, etc.)
LIGAS = [61, 62, 140, 141, 39, 41, 135, 136, 78, 79, 2, 3]

def obtener_datos(endpoint, params=None):
    try:
        url = f"https://v3.football.api-sports.io/{endpoint}"
        res = requests.get(url, headers=HEADERS, params=params).json()
        return res.get('response', [])
    except:
        return []

# --- 4. SELECTOR DE RADAR (BARRA LATERAL) ---
st.sidebar.markdown("""
    <div style="background-color: #1e293b; padding: 15px; border-radius: 10px; border: 1px solid #38bdf8; margin-bottom: 10px; text-align: center;">
        <p style="color: #38bdf8; font-weight: bold; margin: 0; font-size: 16px;">📡 SELECTOR DE RADAR</p>
    </div>
    """, unsafe_allow_html=True)

menu = st.sidebar.pills(
    "Seleccione el tipo de análisis:",
    ["🚀 EN VIVO (Live Analysis)", "📊 PRÓXIMOS (Pre-Match)"],
    selection_mode="single",
    default="📊 PRÓXIMOS (Pre-Match)"
)

# --- 5. FUNCIÓN MAESTRA DE ANÁLISIS ---
def mostrar_analisis_partido(p, es_vivo=False):
    status = f"{p['fixture']['status']['elapsed']}'" if es_vivo else p['fixture']['date'][11:16]
    label_vivo = "🔴 EN VIVO" if es_vivo else "📅"
    
    with st.expander(f"{label_vivo} {status} | {p['teams']['home']['name']} vs {p['teams']['away']['name']}"):
        if st.checkbox("🔍 Cargar Análisis Profundo", key=f"check_{p['fixture']['id']}"):
            tab1, tab2, tab3 = st.tabs(["🎯 Panel Consejos IA", "📈 Estadísticas", "⚔️ H2H"])
            
            with tab1:
                preds_data = obtener_datos("predictions", {"fixture": p['fixture']['id']})
                if preds_data:
                    pred = preds_data[0]
                    # Traducción de IA
                    raw_advice = pred['predictions']['advice']
                    traducciones = {
                        "Home win": "Victoria Local", "Away win": "Victoria Visitante", 
                        "Draw": "Empate", "Double chance": "Doble Oportunidad",
                        "High goals": "Muchos Goles", "Low goals": "Pocos Goles",
                        "expected": "esperados", "draw or": "empate o", "or": "o", "and": "y"
                    }
                    consejo_es = raw_advice
                    for eng, esp in traducciones.items():
                        consejo_es = re.sub(eng, esp, consejo_es, flags=re.IGNORECASE)

                    # Probabilidades
                    pct = pred['predictions']['percent']
                    l_pct, e_pct, v_pct = pct['home'], pct['draw'], pct['away']
                    
                    # Goles
                    texto_goles = pred['predictions'].get('under_over', "Incierto")
                    consejo_gol_color = "#00ff00" if "+" in str(texto_goles) else "#ff4b4b"

                    st.markdown(f"""
                        <div style="background-color: #000000; padding: 25px; border-radius: 15px; border: 3px solid #38bdf8;">
                            <p style="color: white; font-size: 20px;">👑 <b>Ganador Sugerido:</b><br>
                            <span style="color: #facc15; font-size: 24px; font-weight: bold;">{l_pct} Local | {e_pct} Empate | {v_pct} Visita</span></p>
                            
                            <p style="color: white; font-size: 20px;">⚽ <b>Pronóstico Goles:</b><br>
                            <span style="color: {consejo_gol_color}; font-size: 22px; font-weight: bold;">{texto_goles} Goles</span></p>
                            
                            <div style="background-color: #1a1a1a; padding: 15px; border-radius: 10px; border-left: 8px solid #00ff00; margin-top: 15px;">
                                <p style="color: white; font-size: 18px; margin: 0;">💡 <b>VERDICTO FINAL IA:</b><br>
                                <span style="color: #00ff00; font-weight: 900; font-size: 22px; text-transform: uppercase;">{consejo_es}</span></p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            
            with tab2:
                st.subheader("Posiciones y Forma")
                table = obtener_datos("standings", {"league": p['league']['id'], "season": p['league']['season']})
                if table:
                    for team in table[0]['league']['standings'][0][:10]:
                        st.write(f"{team['rank']}. {team['team']['name']} - {team['points']} pts")

            with tab3:
                st.subheader("Historial Cara a Cara (H2H)")
                h2h = obtener_datos("fixtures/headtohead", {"h2h": f"{p['teams']['home']['id']}-{p['teams']['away']['id']}", "last": 5})
                for game in h2h:
                    st.write(f"📅 {game['fixture']['date'][:10]}: {game['teams']['home']['name']} {game['goals']['home']}-{game['goals']['away']} {game['teams']['away']['name']}")

# --- 6. EJECUCIÓN ---
if menu == "🚀 EN VIVO (Live Analysis)":
    partidos = obtener_datos("fixtures", {"live": "all"})
    for p in partidos:
        if p['league']['id'] in LIGAS:
            mostrar_analisis_partido(p, es_vivo=True)
else:
    hoy = date.today().strftime('%Y-%m-%d')
    partidos = obtener_datos("fixtures", {"date": hoy})
    for p in partidos:
        if p['league']['id'] in LIGAS:
            mostrar_analisis_partido(p, es_vivo=False)
