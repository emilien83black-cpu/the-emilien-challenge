import streamlit as st
import random
import cultura, sport, calcio, cinema, intrattenimento, musica

# 1. Configurazione - FIX SCHERMO INTERO
st.set_page_config(page_title="The Emilien Challenge", page_icon="💰", layout="wide")

# 2. Stile CSS - FIX DIMENSIONI MOBILE
st.markdown("""
    <style>
    /* Forza il contenitore a usare il 100% della larghezza */
    .main .block-container {
        max-width: 100% !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    /* Ingrandisce i bottoni per le dita */
    .stButton button {
        height: 3em !important;
        font-size: 18px !important;
    }
    /* Nasconde la barra superiore inutile su mobile */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. Premi e Stato
premi = [100, 200, 300, 500, 1000, 2000, 4000, 8000, 16000, 20000]

if 'indice' not in st.session_state:
    st.session_state.indice = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'fine' not in st.session_state:
    st.session_state.fine = False
if 'usato_5050' not in st.session_state:
    st.session_state.usato_5050 = False
if 'usato_cambio' not in st.session_state:
    st.session_state.usato_cambio = False
if 'usato_suggerimento' not in st.session_state:
    st.session_state.usato_suggerimento = False
if 'opzioni_ridotte' not in st.session_state:
    st.session_state.opzioni_ridotte = None

scelta = st.sidebar.selectbox(
    "Scegli l'argomento:",
    ["Cultura Generale", "Sport Generale", "Calcio", "Cinema", "Intrattenimento Generale", "Musica"]
)

mappa_domande = {
    "Cultura Generale": cultura.domande,
    "Sport Generale": sport.domande,
    "Calcio": calcio.domande,
    "Cinema": cinema.domande,
    "Intrattenimento Generale": intrattenimento.domande,
    "Musica": musica.domande
}

if 'argomento_attuale' not in st.session_state or st.session_state.argomento_attuale != scelta:
    st.session_state.argomento_attuale = scelta
    lista_domande = mappa_domande[scelta].copy()
    random.shuffle(lista_domande)
    for d in lista_domande:
        random.shuffle(d["opzioni"])
    st.session_state.domande = lista_domande
    st.session_state.indice = 0

def usa_5050():
    attuale = st.session_state.domande[st.session_state.indice]
    sbagliate = [o for o in attuale["opzioni"] if o != attuale["corretta"]]
    rimosse = random.sample(sbagliate, 2)
    st.session_state.opzioni_ridotte = [o for o in attuale["opzioni"] if o not in rimosse]
    st.session_state.usato_5050 = True

if not st.session_state.fine:
    attuale = st.session_state.domande[st.session_state.indice]
    
    # Intestazione
    st.markdown(f"<h1 style='text-align: center;'>💰 The Emilien Challenge</h1>", unsafe_allow_html=True)
    
    # Premio e Immagine (Semplificati per mobile)
    col_pre, col_img = st.columns([2, 1])
    with col_pre:
        st.markdown(f"<div style='background-color: black; padding: 10px; border-radius: 5px; text-align: center; border: 1px solid #FFD700;'>Premio: <b style='color: #FFD700;'>{premi[st.session_state.indice]}€</b></div>", unsafe_allow_html=True)
    with col_img:
        import base64
        try:
            with open("Emilien.png", "rb") as f:
                data = base64.b64encode(f.read()).decode("utf-8")
            st.markdown(f'<img src="data:image/png;base64,{data}" width="80">', unsafe_allow_html=True)
        except:
            pass

    st.markdown(f"<div style='text-align: center; font-size: 22px; font-weight: bold; margin-top:10px;'>{attuale['domanda'].replace('#', '')}</div>", unsafe_allow_html=True)
    
    # Aiuti in riga
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("⚖️", disabled=st.session_state.usato_5050, use_container_width=True):
            usa_5050()
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

    # Risposte
    opzioni = st.session_state.opzioni_ridotte if st.session_state.opzioni_ridotte else attuale["opzioni"]
    for i in range(0, len(opzioni), 2):
        riga_a, riga_b = st.columns(2)
        with riga_a:
            if st.button(opzioni[i], key=f"btn_{i}_{st.session_state.indice}", use_container_width=True):
                if opzioni[i] == attuale["corretta"]:
                    st.session_state.indice += 1
                    st.session_state.opzioni_ridotte = None
                    if st.session_state.indice >= 10: st.session_state.fine = True
                    st.rerun()
                else:
                    st.session_state.game_over = True
                    st.session_state.fine = True
                    st.rerun()
        with riga_b:
            if i + 1 < len(opzioni):
                if st.button(opzioni[i+1], key=f"btn_{i+1}_{st.session_state.indice}", use_container_width=True):
                    if opzioni[i+1] == attuale["corretta"]:
                        st.session_state.indice += 1
                        st.session_state.opzioni_ridotte = None
                        if st.session_state.indice >= 10: st.session_state.fine = True
                        st.rerun()
                    else:
                        st.session_state.game_over = True
                        st.session_state.fine = True
                        st.rerun()
else:
    if st.session_state.get('game_over', False):
        st.error("GAME OVER.")
        vincita = premi[st.session_state.indice - 1] if st.session_state.indice > 0 else 0
        st.subheader(f"Te ne vai con: {vincita}€")
    else:
        st.balloons()
        st.success(f"CAMPIONE! Hai vinto {premi[-1]}€!")
    
    if st.button("Ricomincia il gioco", use_container_width=True):
        if 'argomento_attuale' in st.session_state: del st.session_state.argomento_attuale
        st.session_state.indice = 0
        st.session_state.fine = False
        st.session_state.game_over = False
        st.session_state.usato_5050 = False
        st.session_state.usato_cambio = False
        st.session_state.usato_suggerimento = False
        st.session_state.opzioni_ridotte = None
        st.rerun()
