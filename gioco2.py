import streamlit as st
import random
import cultura, sport, calcio, cinema, intrattenimento, musica

# 1. Configurazione
st.set_page_config(page_title="The Emilien Challenge", page_icon="💰", layout="wide")

# 2. Stile CSS Avanzato per forzare il layout Mobile
st.markdown("""
    <style>
    /* Forza le colonne a stare affiancate anche su schermi piccoli */
    [data-testid="column"] {
        width: calc(33% - 1rem) !important;
        flex: 1 1 calc(33% - 1rem) !important;
        min-width: calc(33% - 1rem) !important;
    }

    /* Regola specifica per le risposte (50% di larghezza per fare 2/2) */
    .row-widget.stHorizontal > div:nth-child(2) [data-testid="column"] {
        width: calc(50% - 1rem) !important;
        flex: 1 1 calc(50% - 1rem) !important;
        min-width: calc(50% - 1rem) !important;
    }

    /* Centratura generale */
    .stMarkdown, h1, h2 {
        text-align: center !important;
    }

    /* Rimpicciolisce i bottoni degli aiuti per farli sembrare quadratini */
    .stButton button {
        width: 100% !important;
        height: 2.5em !important;
        font-size: 16px !important;
        padding: 0px !important;
    }

    /* Le risposte restano comode ma proporzionate */
    div.stButton > button[key^="ans_"] {
        height: 3em !important;
        font-size: 15px !important;
    }

    /* Spaziature */
    .block-container { padding-top: 1rem !important; }
    header, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- (Mantieni qui la tua logica di inizializzazione, premi e domande) ---
# [Usa la stessa parte di codice del messaggio precedente per variabili e logica]
if 'indice' not in st.session_state: st.session_state.indice = 0
if 'game_over' not in st.session_state: st.session_state.game_over = False
if 'fine' not in st.session_state: st.session_state.fine = False
if 'usato_5050' not in st.session_state: st.session_state.usato_5050 = False
if 'usato_cambio' not in st.session_state: st.session_state.usato_cambio = False
if 'usato_suggerimento' not in st.session_state: st.session_state.usato_suggerimento = False
if 'opzioni_ridotte' not in st.session_state: st.session_state.opzioni_ridotte = None

scelta = st.sidebar.selectbox("Scegli:", ["Cultura Generale", "Sport Generale", "Calcio", "Cinema", "Intrattenimento Generale", "Musica"])
mappa_domande = {"Cultura Generale": cultura.domande, "Sport Generale": sport.domande, "Calcio": calcio.domande, "Cinema": cinema.domande, "Intrattenimento Generale": intrattenimento.domande, "Musica": musica.domande}

if 'argomento_attuale' not in st.session_state or st.session_state.argomento_attuale != scelta:
    st.session_state.argomento_attuale = scelta
    lista_domande = mappa_domande[scelta].copy()
    random.shuffle(lista_domande)
    for d in lista_domande: random.shuffle(d["opzioni"])
    st.session_state.domande = lista_domande
    st.session_state.indice = 0

def usa_5050():
    attuale = st.session_state.domande[st.session_state.indice]
    sbagliate = [o for o in attuale["opzioni"] if o != attuale["corretta"]]
    rimosse = random.sample(sbagliate, 2)
    st.session_state.opzioni_ridotte = [o for o in attuale["opzioni"] if o not in rimosse]
    st.session_state.usato_5050 = True

# --- LAYOUT CORRETTO ---
if not st.session_state.fine:
    attuale = st.session_state.domande[st.session_state.indice]
    
    st.markdown("<h1>💰 The Emilien Challenge</h1>", unsafe_allow_html=True)
    
    # Logo
    import base64
    try:
        with open("Emilien.png", "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        st.markdown(f'<div style="text-align: center;"><img src="data:image/png;base64,{data}" width="100"></div>', unsafe_allow_html=True)
    except: pass

    st.markdown(f"<h2>🔴 Domanda {st.session_state.indice + 1}</h2>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center; font-size: 18px; font-weight: bold;'>{attuale['domanda'].replace('#', '')}</div>", unsafe_allow_html=True)

    st.write("")

    # 3 AIUTI ORIZZONTALI (Quadratini)
    aiuti_cols = st.columns(3)
    with aiuti_cols[0]:
        if st.button("⚖️", disabled=st.session_state.usato_5050, use_container_width=True):
            usa_5050(); st.rerun()
    with aiuti_cols[1]:
        if st.button("🔄", disabled=st.session_state.usato_cambio, use_container_width=True):
            st.session_state.usato_cambio = True
            st.session_state.indice = (st.session_state.indice + 1) % len(st.session_state.domande)
            st.session_state.opzioni_ridotte = None; st.rerun()
    with aiuti_cols[2]:
        if st.button("💡", disabled=st.session_state.usato_suggerimento, use_container_width=True):
            st.session_state.usato_suggerimento = True; st.toast(attuale["aiuto"], icon="💡")

    st.write("---")

    # 4 RISPOSTE 2x2
    opzioni = st.session_state.opzioni_ridotte if st.session_state.opzioni_ridotte else attuale["opzioni"]
    for i in range(0, len(opzioni), 2):
        r1, r2 = st.columns(2)
        with r1:
            if st.button(opzioni[i], key=f"ans_{i}_{st.session_state.indice}", use_container_width=True):
                if opzioni[i] == attuale["corretta"]:
                    st.session_state.indice += 1; st.session_state.opzioni_ridotte = None
                    if st.session_state.indice >= 10: st.session_state.fine = True
                    st.rerun()
                else: st.session_state.game_over = True; st.session_state.fine = True; st.rerun()
        with r2:
            if i + 1 < len(opzioni):
                if st.button(opzioni[i+1], key=f"ans_{i+1}_{st.session_state.indice}", use_container_width=True):
                    if opzioni[i+1] == attuale["corretta"]:
                        st.session_state.indice += 1; st.session_state.opzioni_ridotte = None
                        if st.session_state.indice >= 10: st.session_state.fine = True
                        st.rerun()
                    else: st.session_state.game_over = True; st.session_state.fine = True; st.rerun()

    # Premio in fondo
    st.markdown(f"<div style='background-color: #000; padding: 5px; border-radius: 10px; text-align: center; border: 1px solid #FFD700; margin-top: 10px;'>Vincita: <b style='color: #FFD700;'>{premi[st.session_state.indice]}€</b></div>", unsafe_allow_html=True)

else:
    # [Schermata finale uguale]
    if st.session_state.get('game_over', False): st.error("GAME OVER")
    else: st.balloons(); st.success("CAMPIONE!")
    if st.button("Ricomincia"):
        if 'argomento_attuale' in st.session_state: del st.session_state.argomento_attuale
        st.session_state.indice = 0; st.session_state.fine = False; st.session_state.game_over = False
        st.session_state.usato_5050 = False; st.session_state.usato_cambio = False
        st.session_state.usato_suggerimento = False; st.session_state.opzioni_ridotte = None; st.rerun()
