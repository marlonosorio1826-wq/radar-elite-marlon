import streamlit as st
import requests
from datetime import date

# 1. ESTILO PROFESIONAL TOTAL Y COLORES
st.set_page_config(page_title="Marlon Pro: Terminal de Apuestas", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .prediction-box { background-color: #1e293b; padding: 15px; border-radius: 10px; border-top: 4px solid #facc15; margin-bottom: 15px; margin-top: 15px; }
    .live-tag { background-color: #ef4444; color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Marlon Pro: Inteligencia Deportiva Total")

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

menu = st.sidebar.radio("Módulo de Análisis:", ["🚀 EN VIVO (Live Analysis)", "📈 PRÓXIMOS (Pre-Match)"])

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
                    
                    # --- NUEVO: PANEL DE CONSEJOS IA ---
                    st.markdown("---")
                    st.markdown("### 🤖 Panel de Consejos IA")
                    
                    # Calculamos el ganador lógico
                    ganador_logico = "Empate"
                    l_val = int(l_pct.replace('%','')) if l_pct != 'N/A' else 0
                    v_val = int(v_pct.replace('%','')) if v_pct != 'N/A' else 0
                    if l_val > v_val and l_val > 40: ganador_logico = f"Local ({p['teams']['home']['name']})"
                    elif v_val > l_val and v_val > 40: ganador_logico = f"Visitante ({p['teams']['away']['name']})"
                    elif l_val > 0: ganador_logico = "Empate / Partido muy cerrado"

                    # Traducimos el consejo de goles
                    consejo_gol_texto = "Apostar al OVER (+2.5) 🟢" if texto_goles == "+2.5" else ("Apostar al UNDER (-2.5) 🔴" if texto_goles == "-2.5" else "Mercado de goles incierto ⚪")

                    st.markdown(f"""
                        <div style="background-color: #0f172a; padding: 20px; border-radius: 10px; border: 1px solid #38bdf8;">
                            <p style="font-size: 16px; margin-bottom: 8px;">👑 <b>Ganador o Doble Chance:</b> La matemática favorece al <b>{ganador_logico}</b>.</p>
                            <p style="font-size: 16px; margin-bottom: 8px;">⚽ <b>Pronóstico de Goles:</b> La IA recomienda <b>{consejo_gol_texto}</b>.</p>
                            <p style="font-size: 16px; margin-bottom: 0px;">💡 <b>Veredicto Final del Algoritmo:</b> <i>"{pred['predictions']['advice']}"</i></p>
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
