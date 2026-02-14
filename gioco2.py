import streamlit as st

# Configurazione per adattare il gioco allo schermo dello smartphone
st.set_page_config(page_title="The Emilien Challenge", layout="wide")

# CSS per rendere testi e bottoni grandi e leggibili su mobile
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
    }
    .stMarkdown p {
        font-size: 22px !important;
        color: white;
    }
    .stButton button {
        width: 100%;
        height: 3.5em;
        font-size: 20px !important;
        margin-bottom: 10px;
    }
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Inizio Logica Gioco
if 'scena' not in st.session_state:
    st.session_state.scena = 'inizio'

def cambia_scena(nuova_scena):
    st.session_state.scena = nuova_scena

scena = st.session_state.scena

if scena == 'inizio':
    st.write("Benvenuto in The Emilien Challenge. La sfida ha inizio.")
    if st.button("Inizia l'avventura"):
        cambia_scena('scelta_1')

elif scena == 'scelta_1':
    st.write("Ti trovi davanti a un bivio. Dove vuoi andare?")
    if st.button("Vai a Sinistra"):
        cambia_scena('sinistra')
    if st.button("Vai a Destra"):
        cambia_scena('destra')

elif scena == 'sinistra':
    st.write("Hai scelto la sinistra. Hai vinto!")
    if st.button("Ricomincia"):
        cambia_scena('inizio')

elif scena == 'destra':
    st.write("Sei caduto in una trappola. Game Over.")
    if st.button("Riprova"):
        cambia_scena('inizio')
