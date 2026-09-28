import streamlit as st
import pandas as pd
from datetime import datetime
import time

# Pagina-instellingen
st.set_page_config(page_title="Rabo Bankieren", page_icon="🔒", layout="centered")

# Volledige Rabobank Styling (Volledig blauw inlogscherm & Witte kaarten)
st.markdown("""
    <style>
    /* Standaard achtergrond voor ingelogd dashboard (Lichtgrijs) */
    .stApp { background-color: #f4f6f8; transition: background-color 0.3s; }
    h1, h2, h3, p, label { font-family: 'Segoe UI', sans-serif !important; }
    
    /* ALS NIET INGELOGD: Forceer de VOLLEDIGE pagina naar diepblauw */
    .unlogged-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background-color: #002d62;
        z-index: -1;
    }
    
    /* Tekst styling voor het blauwe scherm */
    .login-header {
        text-align: center;
        color: white;
        margin-top: 50px;
        margin-bottom: 20px;
    }
    .login-title { color: white !important; font-size: 26px; font-weight: 600; margin-bottom: 8px; }
    .login-subtitle { color: #93c5fd !important; font-size: 15px; margin-bottom: 35px; }
    .pin-dots { font-size: 36px; letter-spacing: 18px; color: #38bdf8; text-align: center; margin-bottom: 30px; }
    
    /* FORCEER RONDE, LICHTE KNOPPEN OP HET BLAUWE SCHERM */
    .blue-theme-active div.stButton > button {
        background-color: rgba(255, 255, 255, 0.15) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        border-radius: 50% !important;
        width: 75px !important;
        height: 75px !important;
        font-size: 26px !important;
        font-weight: 500 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: none !important;
        margin: 12px auto !important;
        padding: 0 !important;
        transition: background-color 0.1s !important;
    }
    .blue-theme-active div.stButton > button:active {
        background-color: rgba(255, 255, 255, 0.3) !important;
    }
    
    /* Wis-knop tekst op blauw scherm */
    .blue-theme-active div.stButton:nth-last-child(3) > button {
        font-size: 16px !important;
        background-color: transparent !important;
        border: none !important;
    }

    /* Forceer kolommen om op mobiel horizontaal te blijven staan */
    [data-testid="column"] {
        width: 33.33% !important;
        flex: 1 1 33.33% !important;
        min-width: 0px !important;
    }
    div[data-testid="stHorizontalBlock"] {
        flex-direction: row !important;
        display: flex !important;
        justify-content: center !important;
        max-width: 320px;
        margin: 0 auto;
    }

    /* Witte kaarten voor het dashboard (Na inloggen) */
    .rabo-card {
        background-color: white;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
        margin-bottom: 15px;
    }
    .card-label { color: #64748b; font-size: 13px; font-weight: 500; text-transform: uppercase; margin-bottom: 4px; }
    .card-value { color: #002d62; font-size: 28px; font-weight: 700; }
    
    /* Verberg Streamlit branding decoraties */
    #MainMenu, footer, header { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# Sessiebeheer
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'pin_input' not in st.session_state:
    st.session_state.pin_input = ""
if 'saldo_betaal' not in st.session_state:
    st.session_state.saldo_betaal = 123.89
if 'saldo_spaar' not in st.session_state:
    st.session_state.saldo_spaar = 5000.00
if 'transacties' not in st.session_state:
    st.session_state.transacties = [
        {"Datum": "29-09-2026", "Omschrijving": "W. Kvits", "Rekening": "NL81RABO0334817293", "Bedrag": -34.20},
        {"Datum": "25-09-2026", "Omschrijving": "Salaris", "Rekening": "NL23INGB0411928374", "Bedrag": 1450.00}
    ]
if 'stap' not in st.session_state:
    st.session_state.stap = "invoeren"

# SCHERM 1: VOLLEDIG BLAUW PINCODE INLOGSCHERM
if not st.session_state.logged_in:
    # Activeer de volledige blauwe achtergrond-hack via CSS class
    st.markdown('<div class="unlogged-bg"></div>', unsafe_allow_html=True)
    
    # Header tekst
    st.markdown("""
        <div class="login-header">
            <div class="login-title">Welkom terug</div>
            <div class="login-subtitle">Voer uw 5-cijferige toegangscode in</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Dynamische rondjes (Ingevuld en leeg)
    ingevuld = len(st.session_state.pin_input)
    rondjes = "● " * ingevuld + "○ " * (5 - ingevuld)
    st.markdown(f'<div class="pin-dots">{rondjes}</div>', unsafe_allow_html=True)
    
    # Start container die de knoppen styling op blauw forceert
    st.markdown('<div class="blue-theme-active">', unsafe_allow_html=True)
    
    # Rij 1
    r1_c1, r1_c2, r1_c3 = st.columns(3)
    with r1_c1:
        if st.button("1", key="k1"): st.session_state.pin_input += "1"; st.rerun()
    with r1_c2:
        if st.button("2", key="k2"): st.session_state.pin_input += "2"; st.rerun()
    with r1_c3:
        if st.button("3", key="k3"): st.session_state.pin_input += "3"; st.rerun()

    # Rij 2
    r2_c1, r2_c2, r2_c3 = st.columns(3)
    with r2_c1:
        if st.button("4", key="k4"): st.session_state.pin_input += "4"; st.rerun()
    with r2_c2:
        if st.button("5", key="k5"): st.session_state.pin_input += "5"; st.rerun()
    with r2_c3:
        if st.button("6", key="k6"): st.session_state.pin_input += "6"; st.rerun()

    # Rij 3
    r3_c1, r3_c2, r3_c3 = st.columns(3)
    with r3_c1:
        if st.button("7", key="k7"): st.session_state.pin_input += "7"; st.rerun()
    with r3_c2:
        if st.button("8", key="k8"): st.session_state.pin_input += "8"; st.rerun()
    with r3_c3:
        if st.button("9", key="k9"): st.session_state.pin_input += "9"; st.rerun()

    # Rij 4
    r4_c1, r4_c2, r4_c3 = st.columns(3)
    with r4_c1:
        if st.button("Wis", key="kwis"): st.session_state.pin_input = ""; st.rerun()
    with r4_c2:
        if st.button("0", key="k0"): st.session_state.pin_input += "0"; st.rerun()
    with r4_c3:
        st.write("") 

    # Sluit de container voor blauwe knoppen styling
    st.markdown('</div>', unsafe_allow_html=True)

    # Pincode controle
    if len(st.session_state.pin_input) == 5:
        if st.session_state.pin_input == "12345":
            st.session_state.logged_in = True
            st.session_state.pin_input = ""
            st.rerun()
        else:
            st.markdown('<p style="color:#f87171; text-align:center; font-weight:600;">Onjuiste toegangscode. Probeer het opnieuw.</p>', unsafe_allow_html=True)
            st.session_state.pin_input = ""
            time.sleep(1.2)
            st.rerun()

# SCHERM 2: STRAK DASHBOARD (INGELOGD - LICHTE MODUS)
else:
    st.markdown("<h2 style='color: #002d62; margin-top:10px; font-weight:700;'>Mijn Rabobank</h2>", unsafe_allow_html=True)
    
    if st.button("Uitloggen", key="logout_btn"):
        st.session_state.logged_in = False
        st.session_state.stap = "invoeren"
        st.rerun()

    tab1, tab2 = st.tabs(["Overzicht", "Geld Overmaken"])

    with tab1:
        st.write("")
        st.markdown(f"""
            <div class="rabo-card">
                <div class="card-label">Rabo Betaalrekening</div>
                <div class="card-value">€ {st.session_state.saldo_betaal:.2f}</div>
                <div style="color: #94a3b8; font-size: 12px; margin-top:5px;">NL81 RABO 0334 8172 93</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="rabo-card">
                <div class="card-label">Rabo Spaarrekening</div>
                <div class="card-value">€ {st.session_state.saldo_spaar:.2f}</div>
                <div style="color: #94a3b8; font-size: 12px; margin-top:5px;">NL92 RABO 0772 1948 41</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h3 style='color: #002d62; font-size: 18px; margin-top: 25px; font-weight:600;'>Transacties</h3>", unsafe_allow_html=True)
        df_transacties = pd.DataFrame(st.session_state.transacties)
        df_transacties['Bedrag'] = df_transacties['Bedrag'].map(lambda x: f"€ {x:.2f}" if x >= 0 else f"- € {abs(x):.2f}")
        st.dataframe(df_transacties, use_container_width=True, hide_index=True)

    with tab2:
        st.write("")
        if st.session_state.stap == "invoeren":
            with st.form("overboeking_form"):
                naam = st.text_input("Naam ontvanger")
                iban = st.text_input("IBAN")
                bedrag = st.number_input("Bedrag (€)", min_value=0.01, format="%.2f")
                omschrijving = st.text_input("Omschrijving (optioneel)")
                
                verzenden = st.form_submit_button("Overboeking controleren")
                
                if verzenden:
                    if not naam or not iban:
                        st.error("Vul de verplichte velden in.")
                    elif bedrag > st.session_state.saldo_betaal:
                        st.error("Saldo onvoldoende op uw Rabo Betaalrekening.")
                    else:
                        st.session_state.temp_transactie = {"naam": naam, "iban": iban, "bedrag": bedrag, "omschrijving": omschrijving}
                        st.session_state.stap = "scanner"
                        st.rerun()

        elif st.session_state.stap == "scanner":
            st.markdown("<div class='rabo-card' style='border-left: 4px solid #ef4444;'><strong>Beveiliging</strong><br>Plaats uw pas in de Rabo Scanner om de overboeking te ondertekenen.</div>", unsafe_allow_html=True)
            t = st.session_state.temp_transactie
            st.write(f"Bedrag: € {t['bedrag']:.2f} naar {t['naam']}")
            
