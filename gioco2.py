import streamlit as st

# FIX VISUALIZZAZIONE MOBILE (Testo grande e schermo intero)
st.set_page_config(page_title="The Emilien Challenge", layout="wide")

st.markdown("""
    <style>
    .main .block-container { max-width: 100% !important; padding: 1rem !important; }
    p, div, span { font-size: 20px !important; }
    .stButton button { width: 100% !important; height: 3em !important; font-size: 18px !important; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- LOGICA ORIGINALE ---
if 'scena' not in st.session_state:
    st.session_state.scena = 'inizio'
if 'aiuti' not in st.session_state:
    st.session_state.aiuti = 3

def cambia_scena(nome):
    st.session_state.scena = nome

# --- SCHERMATA INIZIALE ---
if st.session_state.scena == 'inizio':
    st.image("https://raw.githubusercontent.com/emilien83black-cpu/the-emilien-challenge/main/logo.png", width=300)
    st.title("The Emilien Challenge")
    st.write("Benvenuto nel gioco. Sei pronto ad affrontare la sfida?")
    
    if st.button("Inizia l'Avventura"):
        cambia_scena('scena_1')
    
    st.markdown("---")
    st.write(f"💡 Aiuti rimasti: {st.session_state.aiuti}")
    st.caption("Creato da Emilien - 2026")

# --- SCENA 1 ---
elif st.session_state.scena == 'scena_1':
    st.subheader("Capitolo 1: L'Inizio")
    st.write("Il primo passo è sempre il più difficile. Cosa decidi di fare?")
    
    if st.button("Esplora la zona"):
        cambia_scena('vittoria')
    if st.button("Torna indietro"):
        cambia_scena('sconfitta')
    if st.button("Usa un aiuto") and st.session_state.aiuti > 0:
        st.session_state.aiuti -= 1
        st.info("Suggerimento: Chi non risica non rosica!")

# --- FINALI ---
elif st.session_state.scena == 'vittoria':
    st.success("Complimenti! Hai superato la prima prova.")
    if st.button("Ricomincia"):
        st.session_state.aiuti = 3
        cambia_scena('inizio')

elif st.session_state.scena == 'sconfitta':
    st.error("Peccato! La sfida finisce qui.")
    if st.button("Riprova"):
        st.session_state.aiuti = 3
        cambia_scena('inizio')
