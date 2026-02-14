import streamlit as st

# 1. Forza la pagina a usare tutta la larghezza del telefono e toglie i margini
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# 2. Questo blocco CSS risolve il problema della visualizzazione piccola
st.markdown("""
    <style>
    /* Forza il testo a non essere minuscolo */
    html, body, [data-testid="stverticalblock"] {
        font-size: 20px;
    }
    /* Elimina i bordi bianchi laterali che ti costringono a scorrere col dito */
    .main .block-container {
        padding-top: 1rem;
        padding-right: 1rem;
        padding-left: 1rem;
        max-width: 100%;
    }
    /* Rende i bottoni grandi quanto tutta la larghezza dello schermo */
    .stButton button {
        width: 100%;
        margin-bottom: 10px;
        height: 3em;
        font-size: 18px !important;
    }
    /* Nasconde i menu di Streamlit per pulire la vista */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. Logica del gioco (rimettiamo la tua storia)
if 'scena' not in st.session_state:
    st.session_state.scena = 'inizio'

def vai_a(prossima):
    st.session_state.scena = prossima

scena = st.session_state.scena

if scena == 'inizio':
    st.markdown("### Benvenuto in The Emilien Challenge")
    st.write("La sfida ha inizio. Sei pronto a metterti in gioco?")
    st.button("Inizia l'avventura", on_click=vai_a, args=('scelta_1',))

elif scena == 'scelta_1':
    st.write("Ti trovi davanti a un bivio importante. Da che parte vai?")
    col1, col2 = st.columns(2) # Mette i tasti affiancati se lo schermo è largo, o uno sopra l'altro su mobile
    with col1:
        st.button("SINISTRA", on_click=vai_a, args=('vittoria',))
    with col2:
        st.button("DESTRA", on_click=vai_a, args=('sconfitta',))

elif scena == 'vittoria':
    st.write("## HAI VINTO!")
    st.button("Ricomincia", on_click=vai_a, args=('inizio',))

elif scena == 'sconfitta':
    st.write("## GAME OVER")
    st.button("Riprova", on_click=vai_a, args=('inizio',))
