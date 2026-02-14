import streamlit as st

# Configurazione Pagina
st.set_page_config(page_title="The Emilien Challenge", layout="wide")

# CSS per Mobile (Testo grande e bottoni giganti)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .stMarkdown p { font-size: 26px !important; color: white; text-align: center; }
    .stButton button { 
        width: 100%; 
        height: 4em; 
        font-size: 22px !important; 
        background-color: #ff4b4b; 
        color: white;
        border-radius: 15px;
    }
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Gestione della Memoria del Gioco
if 'scena' not in st.session_state:
    st.session_state.scena = 'inizio'

# Funzione per cambiare scena e ricaricare la pagina
def vai_a(nome_scena):
    st.session_state.scena = nome_scena

# LOGICA DELLE SCENE
scena = st.session_state.scena

if scena == 'inizio':
    st.write("### Benvenuto in The Emilien Challenge")
    st.write("La sfida ha inizio.")
    st.button("Inizia l'avventura", on_click=vai_a, args=('scelta_1',))

elif scena == 'scelta_1':
    st.write("Ti trovi davanti a un bivio. Dove vuoi andare?")
    st.button("Vai a SINISTRA", on_click=vai_a, args=('sinistra',))
    st.button("Vai a DESTRA", on_click=vai_a, args=('destra',))

elif scena == 'sinistra':
    st.write("## HAI VINTO!")
    st.write("Hai scelto la strada giusta.")
    st.button("Ricomincia", on_click=vai_a, args=('inizio',))

elif scena == 'destra':
    st.write("## GAME OVER")
    st.write("Sei caduto in una trappola.")
    st.button("Riprova", on_click=vai_a, args=('inizio',))
