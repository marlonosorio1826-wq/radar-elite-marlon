import streamlit as st
import requests
from datetime import date


# --- CONFIGURACIÓN DE APARIENCIA PROFESIONAL ---
st.set_page_config(page_title="Marlon Pro Elite", layout="wide")

# Ocultar rastro de Streamlit para que parezca una App propia
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    </style>
    """
st.markdown(hide_style, unsafe_allow_html=True)

# --- INICIO DE PÁGINA PERSONALIZADO (FRASE EDITADA) ---
st.markdown("""
    <div style="text-align: center; padding: 25px; background-color: #000000; border-radius: 15px; border: 2px solid #38bdf8; margin-bottom: 30px;">
        <h1 style="color: #ffffff; margin: 0; font-size: 32px; font-family: sans-serif;">🛡️ MARLON PRO ELITE</h1>
        <p style="color: #ffffff; font-size: 20px; font-weight: bold; margin-top: 15px; letter-spacing: 0.5px;">
            Inteligencia y Análisis Aplicado a lo Deportivo
        </p>
        <div style="height: 3px; background: linear-gradient(90deg, #38bdf8, #facc15); width: 60%; margin: 15px auto;"></div>
        <p style="color: #38bdf8; font-size: 14px; text-transform: uppercase; font-weight: bold;">
            Centro de Mando Personalizado
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- CONFIGURACIÓN DE LA CONEXIÓN ---
API_KEY = "b7f271a62e0844b1ac5b1e19638dff75" 
HEADERS = {'x-rapidapi-key': API_KEY, 'x-rapidapi-host': "v3.football.api-sports.io"}

LIGAS = [2, 3, 848, 140, 141, 39, 41, 135, 136, 78, 79, 61, 62]

def obtener_datos(endpoint, params=None):
    try:
        url = f"https://v3.football.api-sports.io/{endpoint}"
        res = requests.get(url, headers=HEADERS, params=params).json()
        if "errors" in res and res["errors"]:
            if isinstance(res["errors"], dict) and "requests" in res["errors"]:
                st.error("⚠️ Límite de API agotado por hoy (100 consultas). Se reiniciará a la medianoche.")
            return []
        return res.get('response', [])
    except: 
        return []

# --- BOTONERA DE NAVEGACIÓN PROFESIONAL ---
st.sidebar.markdown("""
    <div style="background-color: #1e293b; padding: 15px; border-radius: 10px; border: 1px solid #38bdf8; margin-bottom: 20px;">
        <p style="color: #38bdf8; font-size: 14px; font-weight: bold; text-transform: uppercase; text-align: center; margin-bottom: 10px;">
            📡 Selector de Radar
        </p>
    </div>
    """, unsafe_allow_html=True)

# Usamos un estilo de botones segmentados que se ve mucho mejor en móvil
modulo = st.sidebar.pills(
    "Seleccione el tipo de análisis:",
    ["EN VIVO (Live Analysis)", "PRÓXIMOS (Pre-Match)"],
    selection_mode="single",
    default="PRÓXIMOS (Pre-Match)"
)

st.sidebar.markdown("---")

# --- ESTILO PARA HACER LOS BOTONES MÁS GRANDES ---
st.markdown("""
    <style>
    /* Hace que los botones del menú (pills) sean más grandes y fáciles de tocar */
    [data-testid="stBaseButton-pill"] {
        width: 100%;
        height: 50px;
        font-size: 18px !important;
        font-weight: bold !important;
        border: 2px solid #38bdf8 !important;
        background-color: #0f172a !important;
        color: white !important;
        margin-bottom: 10px;
    }
    /* Color cuando el botón está seleccionado */
    [data-testid="stBaseButton-pillActive"] {
        background-color: #38bdf8 !important;
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

def mostrar_analisis_partido(p, es_vivo=False):
    status = f"{p['fixture']['status']['elapsed']}'" if es_vivo else p['fixture']['date'][11:16]
    label_vivo = "🔴 [EN VIVO]" if es_vivo else "📅"
    
    with st.expander(f"{label_vivo} {status} | {p['teams']['home']['name']} {p['goals']['home'] if es_vivo else ''} - {p['goals']['away'] if es_vivo else ''} {p['teams']['away']['name']}"):
        
        if st.checkbox("🔍 Cargar Análisis Profundo", key=f"check_{p['fixture']['id']}"):
            tab1, tab2, tab3 = st.tabs(["💰 Probabilidades & Cuotas", "📊 Estadísticas / Tabla", "⚔️ H2H"])
            
            with tab1:
                st.markdown("### 🎯 Probabilidades Matemáticas (%) y Mercado 1X2")
                
                preds_data = obtener_datos("predictions", {"fixture": p['fixture']['id']})
                odds_data = obtener_datos("odds", {"fixture": p['fixture']['id']})
                
                pred = preds_data[0] if preds_data else None
                
                cuota_l, cuota_e, cuota_v = "-", "-", "-"
                book = None
                if odds_data and odds_data[0]['bookmakers']:
                    book = odds_data[0]['bookmakers'][0] 
                    bet_1x2 = next((b for b in book['bets'] if b['name'] == 'Match Winner'), None)
                    if bet_1x2:
                        vals = bet_1x2['values']
                        cuota_l, cuota_e, cuota_v = vals[0]["odd"], vals[1]["odd"], vals[2]["odd"]

                if pred:
                    pct = pred['predictions']['percent']
                    l_pct = pct.get('home', 'N/A')
                    e_pct = pct.get('draw', 'N/A')
                    v_pct = pct.get('away', 'N/A')
                    
                    c1, c2, c3 = st.columns(3)
                    c1.markdown(f'<div style="text-align:center; background:#1e293b; padding:15px; border-radius:8px; border-top: 4px solid #00ff00;"><p style="color:#cbd5e1; margin:0; font-weight:bold;">LOCAL</p><h1 style="color:#00ff00; margin:5px 0; font-size:36px;">{l_pct}</h1><p style="color:white; margin:0; font-size:18px;">Cuota: <span style="color:#00ff00; font-weight:bold;">{cuota_l}</span></p></div>', unsafe_allow_html=True)
                    c2.markdown(f'<div style="text-align:center; background:#1e293b; padding:15px; border-radius:8px; border-top: 4px solid #94a3b8;"><p style="color:#cbd5e1; margin:0; font-weight:bold;">EMPATE</p><h1 style="color:#ffffff; margin:5px 0; font-size:36px;">{e_pct}</h1><p style="color:white; margin:0; font-size:18px;">Cuota: <span style="font-weight:bold;">{cuota_e}</span></p></div>', unsafe_allow_html=True)
                    c3.markdown(f'<div style="text-align:center; background:#1e293b; padding:15px; border-radius:8px; border-top: 4px solid #3b82f6;"><p style="color:#cbd5e1; margin:0; font-weight:bold;">VISITA</p><h1 style="color:#3b82f6; margin:5px 0; font-size:36px;">{v_pct}</h1><p style="color:white; margin:0; font-size:18px;">Cuota: <span style="color:#3b82f6; font-weight:bold;">{cuota_v}</span></p></div>', unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # --- MERCADO DE GOLES (TARJETAS) ---
                    st.markdown("### ⚽ Mercado de Goles (Línea 2.5)")
                    goles_pred = pred['predictions'].get('under_over', None)
                    texto_goles = goles_pred if goles_pred is not None else "N/A"
                    
                    cuota_over, cuota_under = "-", "-"
                    pct_over, pct_under = "N/A", "N/A"
                    
                    if book:
                        bet_ou = next((b for b in book['bets'] if b['name'] == 'Goals Over/Under'), None)
                        if bet_ou:
                            for val in bet_ou['values']:
                                if val['value'] == 'Over 2.5': cuota_over = val['odd']
                                elif val['value'] == 'Under 2.5': cuota_under = val['odd']
                    
                    try:
                        if cuota_over != "-": pct_over = f"{int((1/float(cuota_over))*100)}%"
                        if cuota_under != "-": pct_under = f"{int((1/float(cuota_under))*100)}%"
                    except: pass
                    
                    col_g1, col_g2, col_g3 = st.columns(3)
                    col_g1.markdown(f'<div style="text-align:center; background:#1e293b; padding:15px; border-radius:8px; border-top: 4px solid #facc15;"><p style="color:#cbd5e1; margin:0; font-weight:bold;">TENDENCIA IA</p><h2 style="color:#facc15; margin:5px 0;">{texto_goles}</h2><p style="color:white; margin:0; font-size:12px;">Pronóstico Algoritmo</p></div>', unsafe_allow_html=True)
                    col_g2.markdown(f'<div style="text-align:center; background:#1e293b; padding:15px; border-radius:8px; border-top: 4px solid #ef4444;"><p style="color:#cbd5e1; margin:0; font-weight:bold;">MÁS DE 2.5 (OVER)</p><h2 style="color:#ef4444; margin:5px 0;">{pct_over}</h2><p style="color:white; margin:0; font-size:16px;">Cuota: <span style="font-weight:bold; color:#ef4444;">{cuota_over}</span></p></div>', unsafe_allow_html=True)
                    col_g3.markdown(f'<div style="text-align:center; background:#1e293b; padding:15px; border-radius:8px; border-top: 4px solid #a855f7;"><p style="color:#cbd5e1; margin:0; font-weight:bold;">MENOS DE 2.5 (UNDER)</p><h2 style="color:#a855f7; margin:5px 0;">{pct_under}</h2><p style="color:white; margin:0; font-size:16px;">Cuota: <span style="font-weight:bold; color:#a855f7;">{cuota_under}</span></p></div>', unsafe_allow_html=True)
                    
                   # --- PANEL DE CONSEJOS IA (VERSIÓN FINAL ALTO CONTRASTE) ---
                    st.markdown("---")
                    st.markdown("### 🤖 Panel de Consejos IA")
                    
                    # 1. TRADUCCIÓN COMPLETA DE CONSEJOS
                    consejo_ia_raw = pred['predictions']['advice']
                    # Diccionario extendido para cubrir todas las frases de la API
                    traducciones = {
                        "Home win": "Victoria Local",
                        "Away win": "Victoria Visitante",
                        "Draw": "Empate",
                        "Double chance": "Doble Oportunidad",
                        "High goals": "Muchos Goles",
                        "Low goals": "Pocos Goles",
                        "expected": "esperados",
                        "draw or": "empate o",
                        "or": "o",
                        "and": "y"
                    }
                    
                    consejo_es = consejo_ia_raw
                    for eng, esp in traducciones.items():
                        # Usamos .lower() para que encuentre las palabras sin importar mayúsculas
                        import re
                        pattern = re.compile(re.escape(eng), re.IGNORECASE)
                        consejo_es = pattern.sub(esp, consejo_es)

                    # 2. CÁLCULO DE GANADOR
                    ganador_logico = "Empate / Incierto"
                    l_val = int(l_pct.replace('%','')) if l_pct != 'N/A' else 0
                    v_val = int(v_pct.replace('%','')) if v_pct != 'N/A' else 0
                    if l_val > v_val and l_val > 40: ganador_logico = f"Local ({p['teams']['home']['name']})"
                    elif v_val > l_val and v_val > 40: ganador_logico = f"Visitante ({p['teams']['away']['name']})"

                    # 3. CONSEJO DE GOLES
                    consejo_gol_texto = "<span style='color:#00ff00;'>Más de 2.5 Goles 🟢</span>" if texto_goles == "+2.5" else ("<span style='color:#ff4b4b;'>Menos de 2.5 Goles 🔴</span>" if texto_goles == "-2.5" else "<span style='color:#ffffff;'>Incierto ⚪</span>")

                    # DISEÑO DE MÁXIMA VISIBILIDAD (FONDO NEGRO, LETRA BLANCA)
                    st.markdown(f"""
                        <div style="background-color: #000000; padding: 25px; border-radius: 15px; border: 3px solid #38bdf8; margin-bottom: 20px;">
                            <p style="font-size: 22px; color: #ffffff !important; margin-bottom: 15px; font-family: Arial, sans-serif;">
                                👑 <b>Ganador Sugerido:</b> <br>
                                <span style="color: #facc15; font-size: 24px; font-weight: 800;">{ganador_logico}</span>
                            </p>
                            <p style="font-size: 22px; color: #ffffff !important; margin-bottom: 15px; font-family: Arial, sans-serif;">
                                ⚽ <b>Pronóstico Goles:</b> <br>
                                <span style="font-weight: 800; font-size: 22px;">{consejo_gol_texto}</span>
                            </p>
                            <div style="background-color: #1a1a1a; padding: 15px; border-radius: 10px; border-left: 8px solid #00ff00;">
                                <p style="font-size: 20px; color: #ffffff !important; margin: 0; font-family: Arial, sans-serif;">
                                    💡 <b>VERDICTO FINAL:</b> <br>
                                    <span style="color: #00ff00; font-weight: 900; font-size: 22px; text-transform: uppercase;">{consejo_es}</span>
                                </p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # 4. MERCADO DOBLE OPORTUNIDAD
                    if book:
                        bet_dc = next((b for b in book['bets'] if b['name'] == 'Double Chance'), None)
                        if bet_dc:
                            st.markdown("🛡️ **Mercado Doble Oportunidad (Cobertura):**")
                            dc_vals = bet_dc['values']
                            dc1, dc2, dc3 = st.columns(3)
                            try:
                                dc1.write(f"{dc_vals[0]['value']}: **{dc_vals[0]['odd']}**")
                                dc2.write(f"{dc_vals[1]['value']}: **{dc_vals[1]['odd']}**")
                                dc3.write(f"{dc_vals[2]['value']}: **{dc_vals[2]['odd']}**")
                            except: pass
                else:
                    st.info("Algoritmo cargando probabilidades...")

            with tab2:
                if es_vivo:
                    st.write("📊 **Presión en Tiempo Real**")
                    stats = obtener_datos("fixtures/statistics", {"fixture": p['fixture']['id']})
                    if stats:
                        for s in stats[0]['statistics']:
                            if s['type'] in ['Ball Possession', 'Total Shots']:
                                st.write(f"{s['type']}: {s['value']}")
                
                st.write(f"🏆 **Posición en Liga**")
                temporada_actual = p['league']['season']
                table = obtener_datos("standings", {"league": p['league']['id'], "season": temporada_actual})
                if table:
                    for team in table[0]['league']['standings'][0][:10]:
                        st.write(f"{team['rank']}. {team['team']['name']} | Pts: {team['points']}")
                else:
                    st.info("Tabla de posiciones no disponible para torneos tipo Copa.")

            with tab3:
                st.write("⚔️ **Historial H2H (Últimos 15 enfrentamientos cruzados)**")
                h2h = obtener_datos("fixtures/headtohead", {"h2h": f"{p['teams']['home']['id']}-{p['teams']['away']['id']}", "last": 15})
                h2h_validos = [g for g in h2h if g['goals']['home'] is not None and g['goals']['away'] is not None]
                
                if h2h_validos:
                    for game in h2h_validos:
                        st.write(f"📅 {game['fixture']['date'][:10]} | {game['teams']['home']['name']} {game['goals']['home']}-{game['goals']['away']} {game['teams']['away']['name']} | 🏆 {game['league']['name']}")
                else:
                    st.warning("⚠️ No se encontraron enfrentamientos recientes en la base de datos central.")

if menu == "🚀 EN VIVO (Live Analysis)":
    st.header("Análisis de Partidos en Curso")
    partidos = obtener_datos("fixtures", {"live": "all"})
    for p in partidos:
        if p['league']['id'] in LIGAS:
            mostrar_analisis_partido(p, es_vivo=True)
else:
    st.header("Análisis Pre-Match: Cartelera de Hoy")
    hoy = date.today().strftime('%Y-%m-%d')
    partidos = obtener_datos("fixtures", {"date": hoy})
    for p in partidos:
        if p['league']['id'] in LIGAS and p['fixture']['status']['short'] == 'NS':
            mostrar_analisis_partido(p, es_vivo=False)
