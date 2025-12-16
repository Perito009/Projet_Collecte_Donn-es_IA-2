import streamlit as st
from auth import logout_button, login_form

st.set_page_config(
    page_title="DataMécanique",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ DataMécanique")
st.caption("L’IA au service de la maintenance prédictive industrielle")

# --- Login / Logout ---
logout_button()
login_form()  # Si pas connecté, bloque ici

# --- Navigation ---
pg = st.navigation([
    st.Page("log.py", title="📝 Logs"),
    st.Page("mesures_capteurs.py", title="📈 Mesures capteurs"),
    st.Page("historiques.py", title="📊 Historique & risques"),
])

# --- Lancement page ---
pg.run()
