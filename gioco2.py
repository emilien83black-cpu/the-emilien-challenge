import streamlit as st
import random
import importlib
import culturagenerale, sport, calcio, cinema, intrattenimento, musica

importlib.reload(culturagenerale)
importlib.reload(sport)
importlib.reload(calcio)
importlib.reload(cinema)
importlib.reload(intrattenimento)
importlib.reload(musica)

# 1. Configurazione
st.set_page_config(page_title="The Emilien Challenge", page_icon="💰", layout="wide")
st.cache_data.clear()

# 2. CSS
st.markdown("""
    <style>
    [data-testid="stVerticalBlock"] { gap: 0,1rem !important; }
    [data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; gap: 4px !important; }
    [data-testid="column"] { flex: 1 !important; min-width: 0px !important; padding: 0px !important; }
    [data-testid="stButton"] { text-align: center; margin-bottom: 0px !important; }
    .stButton button { width: 100% !important; height: 2.0em !important; min-height: 2.0em !important; padding: 0px 5px !important; font-size: 14px !important; border-radius: 4px !important; margin: 0px !important; }
    [data-testid="stVerticalBlock"] > div { padding-bottom: 0px !important; margin-bottom: 1px !important; }
    .centered { text-align: center; }
    header { background-color: transparent !important; height: 2rem !important; }
    .stAppDeployButton, [data-testid="stStatusWidget"], .stActionButton { display: none !important; }
    footer { visibility: hidden; }
    .block-container { padding: 0rem 0.5rem !important; }
    hr { margin-top: 2px !important; margin-bottom: 2px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGICA DI GIOCO ---
if 'indice' not in st.session_state: st.session_state.indice = 0
if 'fine' not in st.session_state: st.session_state.fine = False
if 'game_over' not in st.session_state: st.session_state.game_over = False
if 'mostra_errore' not in st.session_state: st.session_state.mostra_errore = False
if 'usato_5050' not in st.session_state: st.session_state.usato_5050 = False
if 'usato_cambio' not in st.session_state: st.session_state.usato_cambio = False
if 'usato_suggerimento' not in st.session_state: st.session_state.usato_suggerimento = False
if 'opzioni_ridotte' not in st.session_state: st.session_state.opzioni_ridotte = None

premi = [100, 200, 300, 500, 1000, 2000, 4000, 8000, 16000, 20000]

scelta = st.sidebar.selectbox("Scegli:", ["Cultura Generale", "Sport Generale", "Calcio", "Cinema", "Intrattenimento Generale", "Musica"])
mappa_domande = {"Cultura Generale": culturagenerale.domande, "Sport Generale": sport.domande, "Calcio": calcio.domande, "Cinema": cinema.domande, "Intrattenimento Generale": intrattenimento.domande, "Musica": musica.domande}

if 'argomento_attuale' not in st.session_state or st.session_state.argomento_attuale != scelta:
    st.session_state.argomento_attuale = scelta
    lista = mappa_domande[scelta].copy()
    random.shuffle(lista)
    for d in lista: random.shuffle(d["opzioni"])
    st.session_state.domande = lista
    st.session_state.indice = 0

if not st.session_state.fine:
    attuale = st.session_state.domande[st.session_state.indice]
    st.markdown("<h1 class='centered'>💰 The Emilien Challenge</h1>", unsafe_allow_html=True)
    
    import base64
    try:
        with open("Emilien.png", "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        st.markdown(f'<div class="centered"><img src="data:image/png;base64,{data}" width="100"></div>', unsafe_allow_html=True)
    except: pass

    if st.session_state.mostra_errore:
        st.markdown(f"<div style='background-color: #ff4b4b; padding: 20px; border-radius: 10px; color: white; text-align: center; margin-bottom: 20px;'><h3>Sbagliato!</h3><p>La risposta corretta era: <b>{attuale['corretta']}</b></p><p><i>{attuale.get('spiegazione', 'Nessun commento disponibile.')}</i></p></div>", unsafe_allow_html=True)
        if st.button("Continua", use_container_width=True):
            st.session_state.game_over = True
            st.session_state.fine = True
            st.rerun()
    else:
        st.markdown(f"<h2 class='centered'>🔴 Domanda {st.session_state.indice + 1}</h2>", unsafe_allow_html=True)
        st.markdown(f"<div class='centered' style='font-size: 18px; font-weight: bold; padding: 5px;'>{attuale['domanda'].replace('#', '')}</div>", unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("⚖️", disabled=st.session_state.usato_5050, use_container_width=True):
                st.session_state.usato_5050 = True
                sbagliate = [o for o in attuale["opzioni"] if o != attuale["corretta"]]
                st.session_state.opzioni_ridotte = [attuale["corretta"], random.choice(sbagliate)]
                st.rerun()
        with c2:
            if st.button("🔄", disabled=st.session_state.usato_cambio, use_container_width=True):
                st.session_state.usato_cambio = True
                st.session_state.indice = (st.session_state.indice + 1) % len(st.session_state.domande)
                st.session_state.opzioni_ridotte = None
                st.rerun()
        with c3:
            if st.button("💡", disabled=st.session_state.usato_suggerimento, use_container_width=True):
                st.session_state.usato_suggerimento = True
                st.toast(attuale["aiuto"], icon="💡")

        opz = st.session_state.opzioni_ridotte if st.session_state.opzioni_ridotte else attuale["opzioni"]
        
        for i in range(0, len(opz), 2):
            r_col1, r_col2 = st.columns(2)
            with r_col1:
                if st.button(opz[i], key=f"a_{i}", use_container_width=True):
                    if opz[i] == attuale["corretta"]:
                        st.session_state.indice += 1
                        st.session_state.opzioni_ridotte = None
                        if st.session_state.indice >= 10: st.session_state.fine = True
                        st.rerun()
                    else:
                        st.session_state.mostra_errore = True
                        st.rerun()
            with r_col2:
                if i + 1 < len(opz):
                    if st.button(opz[i+1], key=f"a_{i+1}", use_container_width=True):
                        if opz[i+1] == attuale["corretta"]:
                            st.session_state.indice += 1
                            st.session_state.opzioni_ridotte = None
                            if st.session_state.indice >= 10: st.session_state.fine = True
                            st.rerun()
                        else:
                            st.session_state.mostra_errore = True
                            st.rerun()

        st.markdown(f"<div style='background-color: #000; padding: 10px; border-radius: 5px; text-align: center; border: 1px solid gold; margin-top: 10px;'>Vincita: {premi[st.session_state.indice]}€</div>", unsafe_allow_html=True)

else:
    if st.session_state.get('game_over', False): st.error("GAME OVER")
    else: st.balloons(); st.success("CAMPIONE!")
    if st.button("Ricomincia"):
        for key in ['indice', 'fine', 'game_over', 'mostra_errore', 'usato_5050', 'usato_cambio', 'usato_suggerimento', 'opzioni_ridotte', 'argomento_attuale']:
            if key in st.session_state: del st.session_state[key]
        st.rerun()






