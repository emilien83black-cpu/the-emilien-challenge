import streamlit as st
import random
import cultura, sport, calcio, cinema, intrattenimento, musica

# 1. Configurazione (DEVE stare qui, in cima a tutto)
st.set_page_config(page_title="The Emilien Challenge", page_icon="💰")

# 2. Stile CSS
st.markdown("""
    <style>
    .block-container {
        padding-top: 3rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Premi e Stato
premi = [100, 200, 300, 500, 1000, 2000, 4000, 8000, 16000, 20000]

# Inizializzazione di TUTTE le variabili di stato (così non crasha mai all'avvio)
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
# 2. MAPPA DEI FILE ESTERNI
mappa_domande = {
    "Cultura Generale": cultura.domande,
    "Sport Generale": sport.domande,
    "Calcio": calcio.domande,
    "Cinema": cinema.domande,
    "Intrattenimento Generale": intrattenimento.domande,
    "Musica": musica.domande
}

import random

# 3. RESET AUTOMATICO AL CAMBIO CATEGORIA
if 'argomento_attuale' not in st.session_state or st.session_state.argomento_attuale != scelta:
    st.session_state.argomento_attuale = scelta
    
    # Creiamo una copia per non mescolare il file originale
    lista_domande = mappa_domande[scelta].copy()
    
    # 1. Rimescoliamo l'ordine delle domande
    random.shuffle(lista_domande)
    
    # 2. Rimescoliamo le opzioni dentro ogni singola domanda
    for d in lista_domande:
        random.shuffle(d["opzioni"])
    
    st.session_state.domande = lista_domande
    st.session_state.indice = 0
    # ... tutto il resto che avevi già (punteggio, fine, aiuti, ecc.) ...

# 4. FUNZIONE AIUTO 50/50
def usa_5050():
    attuale = st.session_state.domande[st.session_state.indice]
    sbagliate = [o for o in attuale["opzioni"] if o != attuale["corretta"]]
    rimosse = random.sample(sbagliate, 2)
    st.session_state.opzioni_ridotte = [o for o in attuale["opzioni"] if o not in rimosse]
    st.session_state.usato_5050 = True

# 5. LOGICA DEL GIOCO
if not st.session_state.fine:
    attuale = st.session_state.domande[st.session_state.indice]
    
    # Intestazione centrata con immagine a destra
    testa1, testa2 = st.columns([4, 1])
    with testa1:
        st.markdown(f"<h1 style='text-align: center;'>💰 The Emilien Challenge</h1>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center;'>Categoria: {scelta}</h3>", unsafe_allow_html=True)
    with testa2:
        import base64
        try:
            with open("Emilien.png", "rb") as f:
                data = base64.b64encode(f.read()).decode("utf-8")
            st.markdown(f'<img src="data:image/png;base64,{data}" width="120">', unsafe_allow_html=True)
        except:
            pass

    # Domanda centrata con rimozione automatica hashtag
    st.markdown(f"<h2 style='text-align: center;'>🔴 Domanda {st.session_state.indice + 1}</h2>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center; font-size: 24px; font-weight: bold;'>{attuale['domanda'].replace('#', '')}</div>", unsafe_allow_html=True)
    
    st.write("") # Spazio vuoto

    # Zona centrale: Aiuti a sinistra, Risposte in mezzo, Premio a destra
    col_sx, col_centro, col_dx = st.columns([1, 4, 1])

    with col_sx:
        if st.button("⚖️", help="50/50", disabled=st.session_state.usato_5050, use_container_width=True):
            usa_5050()
            st.rerun()
        if st.button("🔄", help="Cambio", disabled=st.session_state.usato_cambio, use_container_width=True):
            st.session_state.usato_cambio = True
            st.session_state.indice = (st.session_state.indice + 1) % len(st.session_state.domande)
            st.session_state.opzioni_ridotte = None
            st.rerun()
        if st.button("💡", help="Indizio", disabled=st.session_state.usato_suggerimento, use_container_width=True):
            st.session_state.usato_suggerimento = True
            st.toast(attuale["aiuto"], icon="💡")

    with col_centro:
        opzioni = st.session_state.opzioni_ridotte if st.session_state.opzioni_ridotte else attuale["opzioni"]
        for i in range(0, len(opzioni), 2):
            riga_a, riga_b = st.columns(2)
            with riga_a:
                opc = opzioni[i]
                if st.button(opc, key=f"{opc}_{st.session_state.indice}", use_container_width=True):
                    if opc == attuale["corretta"]:
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
                    opc2 = opzioni[i+1]
                    if st.button(opc2, key=f"{opc2}_{st.session_state.indice}", use_container_width=True):
                        if opc2 == attuale["corretta"]:
                            st.session_state.indice += 1
                            st.session_state.opzioni_ridotte = None
                            if st.session_state.indice >= 10: st.session_state.fine = True
                            st.rerun()
                        else:
                            st.session_state.game_over = True
                            st.session_state.fine = True
                            st.rerun()

    with col_dx:
        st.markdown(f"<div style='background-color: black; padding: 10px; border-radius: 5px; text-align: center; border: 1px solid #FFD700;'>Premio attuale:<br><b style='color: #FFD700;'>{premi[st.session_state.indice]}€</b></div>", unsafe_allow_html=True)

# 6. RISULTATO FINALE 
else:
    if st.session_state.get('game_over', False):
        st.error("GAME OVER.")
        vincita = premi[st.session_state.indice - 1] if st.session_state.indice > 0 else 0
        st.subheader(f"Te ne vai con: {vincita}€")
    else:
        st.balloons()
        st.success(f"CAMPIONE! Hai completato la scalata e vinto {premi[-1]}€!")
    
    if st.button("Ricomincia il gioco", use_container_width=True):
        # Rimuoviamo l'argomento attuale così il RESET AUTOMATICO si attiva
        if 'argomento_attuale' in st.session_state:
            del st.session_state.argomento_attuale
        
        # Resettiamo tutto il resto
        st.session_state.indice = 0
        st.session_state.fine = False
        st.session_state.game_over = False
        st.session_state.usato_5050 = False
        st.session_state.usato_cambio = False
        st.session_state.usato_suggerimento = False
        st.session_state.opzioni_ridotte = None
        st.rerun()