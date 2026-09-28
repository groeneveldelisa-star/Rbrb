import streamlit as st
import pandas as pd
from datetime import datetime
import time

# Pagina-instellingen en Rabobank-stijl
st.set_page_config(page_title="Rabo Online Bankieren", page_icon="🏦", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f4f6f8; }
    h1, h2, h3 { color: #002d62; font-family: 'Segoe UI', sans-serif; }
    .stButton>button {
        background-color: #ff5f00;
        color: white;
        border-radius: 4px;
        border: none;
        padding: 10px 24px;
        width: 100%;
    }
    .stButton>button:hover { background-color: #e05300; color: white; }
    </style>
""", unsafe_allow_html=True)


# Sessiebeheer (Gegevensopslag binnen de sessie)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'saldo_betaal' not in st.session_state:
    st.session_state.saldo_betaal = 1250.45
if 'saldo_spaar' not in st.session_state:
    st.session_state.saldo_spaar = 5000.00
if 'transacties' not in st.session_state:
    st.session_state.transacties = [
        {"Datum": "28-09-2026", "Naam/Omschrijving": "Albert Heijn", "Rekening": "NL81RABO0334817293", "Bedrag": -34.20},
        {"Datum": "25-09-2026", "Naam/Omschrijving": "Salaris Werkgever", "Rekening": "NL23INGB0411928374", "Bedrag": 1450.00}
    ]

# SCHERM 1: INLOGGEN
if not st.session_state.logged_in:
    st.title("🏦 Rabo Online Bankieren")
    st.subheader("Welkom bij Rabo Online Bankieren")
    
    with st.form("login_form"):
        rekeningnummer = st.text_input("Rekeningnummer of Pasnummer", value="NL81 RABO 0334 8172 93")
        toegangscode = st.text_input("Toegangscode", type="password")
        submit_login = st.form_submit_button("Veilig inloggen")
        
        if submit_login:
            if toegangscode == "1234":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Onjuiste toegangscode. Controleer uw gegevens en probeer het opnieuw.")

# SCHERM 2: DASHBOARD (INGELOGD)
else:
        col_logo, col_logout = st.columns(2)

    with col_logo:
        st.title("🍊 Mijn Rabo")
    with col_logout:
        if st.button("Uitloggen"):
            st.session_state.logged_in = False
            st.rerun()

    tab1, tab2 = st.tabs(["📊 Overzicht", "💸 Geld Overmaken"])

    # TAB 1: REKENINGOVERSZICHT
    with tab1:
        st.subheader("Uw rekeningen")
        st.metric(label="Rabo Betaalrekening (NL81 RABO 0334 8172 93)", value=f"€ {st.session_state.saldo_betaal:.2f}")
        st.metric(label="Rabo Spaarrekening (NL92 RABO 0772 1948 41)", value=f"€ {st.session_state.saldo_spaar:.2f}")
        
        st.write("---")
        st.subheader("🔄 Recente af- en bijschrijvingen")
        df_transacties = pd.DataFrame(st.session_state.transacties)
        df_transacties['Bedrag'] = df_transacties['Bedrag'].map(lambda x: f"€ {x:.2f}" if x >= 0 else f"- € {abs(x):.2f}")
        st.dataframe(df_transacties, use_container_width=True, hide_index=True)

    # TAB 2: GELD OVERMAKEN
    with tab2:
        st.subheader("Nieuwe overboeking")
        
        with st.form("overboeking_form"):
            naam = st.text_input("Naam ontvanger")
            iban = st.text_input("IBAN (Rekeningnummer)")
            bedrag = st.number_input("Bedrag (€)", min_value=0.01, format="%.2f")
            omschrijving = st.text_input("Omschrijving")
            
            verzenden = st.form_submit_button("Overboeking controleren")
            
            if verzenden:
                if not naam or not iban:
                    st.error("Vul alle verplichte velden in.")
                elif bedrag > st.session_state.saldo_betaal:
                    st.error("⚠️ Saldo onvoldoende op uw Rabo Betaalrekening.")
                else:
                    st.session_state.temp_transactie = {"naam": naam, "iban": iban, "bedrag": bedrag, "omschrijving": omschrijving}
                    st.session_state.stap = "scanner"

        # Rabo Scanner verificatie
        if 'stap' in st.session_state and st.session_state.stap == "scanner":
            st.warning("🔒 **Rabo Scanner**")
            st.write("Plaats uw Rabo Wereldpas in de Rabo Scanner en genereer een signeercode.")
            
            rabo_code = st.text_input("Signiércode (8 cijfers)", type="password")
            if st.button("Bevestig met Rabo Scanner"):
                if rabo_code == "9999":
                    t = st.session_state.temp_transactie
                    st.session_state.saldo_betaal -= t['bedrag']
                    st.session_state.transacties.insert(0, {
                        "Datum": datetime.now().strftime("%d-%m-%Y"),
                        "Naam/Omschrijving": t['naam'],
                        "Rekening": t['iban'],
                        "Bedrag": -float(t['bedrag'])
                    })
                    st.success("De overboeking is succesvol verwerkt.")
                    time.sleep(1.5)
                    del st.session_state.stap
                    st.rerun()
                else:
                    st.error("De ingevoerde signeercode is onjuist. Probeer het opnieuw.")
