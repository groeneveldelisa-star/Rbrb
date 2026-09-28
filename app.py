import streamlit as st
import pandas as pd
from datetime import datetime
import time

# Pagina-instellingen
st.set_page_config(page_title="Rabo Bankieren", page_icon="🔒", layout="centered")

# Volledige Rabobank Styling (Blauw inlogscherm & Witte kaarten)
st.markdown("""
    <style>
    /* Algemene achtergrond */
    .stApp { background-color: #f4f6f8; }
    
    /* Titels en teksten */
    h1, h2, h3, p, label { font-family: 'Segoe UI', sans-serif !important; }
    
    /* Styling voor het blauwe inlogscherm */
    .login-container {
        background-color: #002d62;
        padding: 40px 30px;
        border-radius: 16px;
        text-align: center;
        color: white;
        margin-top: 20px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
    }
    .login-title { color: white !important; font-size: 24px; font-weight: 600; margin-bottom: 5px; }
    .login-subtitle { color: #cbd5e1 !important; font-size: 14px; margin-bottom: 25px; }
    
    /* Pincode bolletjes */
    .pin-dots { font-size: 28px; letter-spacing: 12px; margin-bottom: 25px; color: #38bdf8; }
    
    /* Witte kaarten voor het dashboard */
    .rabo-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .card-label { color: #64748b; font-size: 13px; font-weight: 500; text-transform: uppercase; margin-bottom: 4px; }
    .card-value { color: #002d62; font-size: 28px; font-weight: 700; }
    
    /* Strakke knoppen zonder oranje */
    .stButton>button {
        background-color: #002d62;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 12px;
        font-weight: 600;
        width: 100%;
        transition: background-color 0.2s;
    }
    .stButton>button:hover { background-color: #001f44; color: white; }
    
    /* Cijfertoetsenbord knoppen */
    .num-pad button {
        background-color: rgba(255,255,255,0.1) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 50% !important;
        width: 60px !important;
        height: 60px !important;
        font-size: 20px !important;
        margin: 10px auto !important;
    }
    .num-pad button:hover { background-color: rgba(255,255,255,0.2) !important; }
    </style>
""", unsafe_allow_html=True)

# Sessiebeheer
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'pin_input' not in st.session_state:
    st.session_state.pin_input = ""
if 'saldo_betaal' not in st.session_state:
    st.session_state.saldo_betaal = 123.89  # Aangepast naar jouw foto!
if 'saldo_spaar' not in st.session_state:
    st.session_state.saldo_spaar = 5000.00
if 'transacties' not in st.session_state:
    st.session_state.transacties = [
        {"Datum": "29-09-2026", "Omschrijving": "W. Kvits", "Rekening": "NL81RABO0334817293", "Bedrag": -34.20},
        {"Datum": "25-09-2026", "Omschrijving": "Salaris", "Rekening": "NL23INGB0411928374", "Bedrag": 1450.00}
    ]
if 'stap' not in st.session_state:
    st.session_state.stap = "invoeren"

# SCHERM 1: BLAUW PINCODE INLOGSCHERM
if not st.session_state.logged_in:
    # Gecentreerde container maken
    col_space1, col_content, col_space2 = st.columns([1, 6, 1])
    
    with col_content:
        # Weergave van de ingevulde rondjes
        ingevuld = len(st.session_state.pin_input)
        rondjes = "● " * ingevuld + "○ " * (5 - ingevuld)
        
        st.markdown(f"""
            <div class="login-container">
                <div class="login-title">Welkom terug</div>
                <div class="login-subtitle">Voer uw 5-cijferige toegangscode in</div>
                <div class="pin-dots">{rondjes}</div>
            </div>
        """, unsafe_allowed_html=True)
        
        # Cijfertoetsenbord bouwen (3 kolommen per rij)
        st.write("")
        c1, c2, c3 = st.columns(3)
        
        with c1:
            if st.button("1", key="btn1"): st.session_state.pin_input += "1"; st.rerun()
            if st.button("4", key="btn4"): st.session_state.pin_input += "4"; st.rerun()
            if st.button("7", key="btn7"): st.session_state.pin_input += "7"; st.rerun()
            if st.button("Wis", key="btn_wis"): st.session_state.pin_input = ""; st.rerun()
        with c2:
            if st.button("2", key="btn2"): st.session_state.pin_input += "2"; st.rerun()
            if st.button("5", key="btn5"): st.session_state.pin_input += "5"; st.rerun()
            if st.button("8", key="btn8"): st.session_state.pin_input += "8"; st.rerun()
            if st.button("0", key="btn0"): st.session_state.pin_input += "0"; st.rerun()
        with c3:
            if st.button("3", key="btn3"): st.session_state.pin_input += "3"; st.rerun()
            if st.button("6", key="btn6"): st.session_state.pin_input += "6"; st.rerun()
            if st.button("9", key="btn9"): st.session_state.pin_input += "9"; st.rerun()
            
        # Pincode controle (Pincode is nu 5 cijfers: 12345)
        if len(st.session_state.pin_input) == 5:
            if st.session_state.pin_input == "12345":
                st.session_state.logged_in = True
                st.session_state.pin_input = ""
                st.rerun()
            else:
                st.error("Onjuiste toegangscode. Probeer het opnieuw.")
                st.session_state.pin_input = ""
                time.sleep(1)
                st.rerun()

# SCHERM 2: STRAK DASHBOARD (INGELOGD)
else:
    col_title, col_btn = st.columns([3, 1])
    with col_title:
        st.markdown("<h2 style='color: #002d62; margin-top:10px;'>Mijn Rabobank</h2>", unsafe_allow_html=True)
    with col_btn:
        st.write("")
        if st.button("Uitloggen"):
            st.session_state.logged_in = False
            st.session_state.stap = "invoeren"
            st.rerun()

    tab1, tab2 = st.tabs(["Overzicht", "Geld Overmaken"])

    # TAB 1: REKENINGOVERSZICHT (Met witte kaarten-stijl)
    with tab1:
        st.write("")
        
        # Betaalrekening Kaart
        st.markdown(f"""
            <div class="rabo-card">
                <div class="card-label">Rabo Betaalrekening</div>
                <div class="card-value">€ {st.session_state.saldo_betaal:.2f}</div>
                <div style="color: #94a3b8; font-size: 12px; margin-top:5px;">NL81 RABO 0334 8172 93</div>
            </div>
        """, unsafe_allowed_html=True)
        
        # Spaarrekening Kaart
        st.markdown(f"""
            <div class="rabo-card">
                <div class="card-label">Rabo Spaarrekening</div>
                <div class="card-value">€ {st.session_state.saldo_spaar:.2f}</div>
                <div style="color: #94a3b8; font-size: 12px; margin-top:5px;">NL92 RABO 0772 1948 41</div>
            </div>
        """, unsafe_allowed_html=True)
        
        st.markdown("<h3 style='color: #002d62; font-size: 18px; margin-top: 25px;'>Transacties</h3>", unsafe_allow_html=True)
        df_transacties = pd.DataFrame(st.session_state.transacties)
        df_transacties['Bedrag'] = df_transacties['Bedrag'].map(lambda x: f"€ {x:.2f}" if x >= 0 else f"- € {abs(x):.2f}")
        st.dataframe(df_transacties, use_container_width=True, hide_index=True)

    # TAB 2: GELD OVERMAKEN
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

        # Rabo Scanner verificatiescherm
        elif st.session_state.stap == "scanner":
            st.markdown("<div class='rabo-card' style='border-left: 4px solid #ef4444;'><strong>Beveiliging</strong><br>Plaats uw pas in de Rabo Scanner om de overboeking te ondertekenen.</div>", unsafe_allow_html=True)
            t = st.session_state.temp_transactie
            st.write(f"Bedrag: € {t['bedrag']:.2f} naar {t['naam']}")
            
            with st.form("scanner_form"):
                rabo_code = st.text_input("Signeercode", type="password")
                bevestig = st.form_submit_button("Bevestig overboeking")
                
                if bevestig:
                    if rabo_code == "9999":
                        st.session_state.saldo_betaal -= t['bedrag']
                        st.session_state.transacties.insert(0, {
                            "Datum": datetime.now().strftime("%d-%m-%Y"),
                            "Omschrijving": t['naam'],
                            "Rekening": t['iban'],
                            "Bedrag": -float(t['bedrag'])
                        })
                        st.success("De overboeking is succesvol verwerkt.")
                        time.sleep(1.5)
                        st.session_state.stap = "invoeren"
                        st.rerun()
                    else:
                        st.error("Onjuiste signeercode.")
            
            if st.button("Annuleren"):
                st.session_state.stap = "invoeren"
                st.rerun()
