import streamlit as st
import random
import cultura, sport, calcio, cinema, intrattenimento, musica

# 1. Configurazione (Layout Wide è fondamentale)
st.set_page_config(page_title="The Emilien Challenge", page_icon="💰", layout="wide")

# 2. Stile CSS per centrare tutto e sistemare i bottoni
st.markdown("""
    <style>
    /* Centra il testo e le immagini */
    .stMarkdown, .stImage, h1, h2, h3 {
        text-align: center !important;
        display: flex;
        justify-content: center;
    }
    
    /* Forza il logo al centro */
    [data-testid="stImage"] img {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }

    /* Rende i bottoni delle risposte e degli aiuti più grandi e leggibili */
    .stButton button {
        width: 100% !important;
        height: 3.5em !important;
        font-size: 18px !important;
        margin-bottom: 5px !important;
    }
    
    /* Rimuove lo spazio vuoto in alto */
    .block-container {
        padding-top: 1rem !important;
    }

    /* Nasconde la barra di Streamlit per pulizia */
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- (Qui mantieni tutta la tua parte di inizializzazione variabili, premi e mappa_domande uguale a prima) ---
premi = [100, 200, 300, 500, 1000, 2000, 4000, 8000, 16000, 20000]
if 'indice' not in st.session_state: st.session_state.indice = 0
if 'game_over' not in st.session_state: st.session_state.game_over = False
if 'fine' not in st.session_state: st.session_state.fine = False
if 'usato_5050' not in st.session_state: st.session_state.usato_5050 = False
if 'usato_cambio' not in st.session_state: st.session_state.usato_cambio = False
if 'usato_suggerimento' not in st.session_state: st.session_state.usato_suggerimento = False
if 'opzioni_ridotte' not in st.session_state: st.session_state.opzioni_ridotte = None

scelta = st.sidebar.selectbox("Scegli l'argomento:", ["Cultura Generale", "Sport Generale", "Calcio", "Cinema", "Intrattenimento Generale", "Musica"])
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

# --- LOGICA VISIVA ---
if not st.session_state.fine:
    attuale = st.session_state.domande[st.session_state.indice]
    
    # Titolo e Logo centrati
    st.markdown("<h1>💰 The Emilien Challenge</h1>", unsafe_allow_html=True)
    
    import base64
    try:
        with open("Emilien.png", "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        st.markdown(f'<div style="text-align: center;"><img src="data:image/png;base64,{data}" width="120"></div>', unsafe_allow_html=True)
    except:
        pass

    # Numero domanda con pallino rosso e Domanda
    st.markdown(f"<h2 style='color: white;'>🔴 Domanda {st.session_state.indice + 1}</h2>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center; font-size: 22px; font-weight: bold; margin-bottom: 20px;'>{attuale['domanda'].replace('#', '')}</div>", unsafe_allow_html=True)

    # 3 Aiuti in Orizzontale (3 colonne)
    col_a1, col_a2, col_a3 = st.columns(3)
    with col_a1:
        if st.button("⚖️", disabled=st.session_state.usato_5050, use_container_width=True):
            usa_5050(); st.rerun()
    with col_a2:
        if st.button("🔄", disabled=st.session_state.usato_cambio, use_container_width=True):
            st.session_state.usato_cambio = True
            st.session_state.indice = (st.session_state.indice + 1) % len(st.session_state.domande)
            st.session_state.opzioni_ridotte = None; st.rerun()
    with col_a3:
        if st.button("💡", disabled=st.session_state.usato_suggerimento, use_container_width=True):
            st.session_state.usato_suggerimento = True; st.toast(attuale["aiuto"], icon="💡")

    st.write("---") # Separatore

    # 4 Risposte 2 sopra e 2 sotto
    opzioni = st.session_state.opzioni_ridotte if st.session_state.opzioni_ridotte else attuale["opzioni"]
    for i in range(0, len(opzioni), 2):
        r1, r2 = st.columns(2)
        with r1:
            if st.button(opzioni[i], key=f"ans_{i}", use_container_width=True):
                if opzioni[i] == attuale["corretta"]:
                    st.session_state.indice += 1
                    st.session_state.opzioni_ridotte = None
                    if st.session_state.indice >= 10: st.session_state.fine = True
                    st.rerun()
                else:
                    st.session_state.game_over = True; st.session_state.fine = True; st.rerun()
        with r2:
            if i + 1 < len(opzioni):
                if st.button(opzioni[i+1], key=f"ans_{i+1}", use_container_width=True):
                    if opzioni[i+1] == attuale["corretta"]:
                        st.session_state.indice += 1
                        st.session_state.opzioni_ridotte = None
                        if st.session_state.indice >= 10: st.session_state.fine = True
                        st.rerun()
                    else:
                        st.session_state.game_over = True; st.session_state.fine = True; st.rerun()

    # Premio attuale in fondo centrato
    st.markdown(f"<div style='background-color: #1e1e1e; padding: 10px; border-radius: 10px; text-align: center; border: 2px solid #FFD700; margin-top: 20px;'>Premio Attuale: <b style='color: #FFD700;'>{premi[st.session_state.indice]}€</b></div>", unsafe_allow_html=True)

else:
    # (Parte finale Game Over / Vittoria uguale a prima)
    if st.session_state.get('game_over', False):
        st.error("GAME OVER")
    else:
        st.balloons(); st.success("CAMPIONE!")
    if st.button("Ricomincia"):
        if 'argomento_attuale' in st.session_state: del st.session_state.argomento_attuale
        st.session_state.indice = 0; st.session_state.fine = False; st.session_state.game_over = False
        st.session_state.usato_5050 = False; st.session_state.usato_cambio = False
        st.session_state.usato_suggerimento = False; st.session_state.opzioni_ridotte = None; st.rerun()
