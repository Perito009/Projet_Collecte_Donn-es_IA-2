import streamlit as st
from auth import logout_button, login_form

st.set_page_config(
    page_title="DataMécanique",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Barre en haut avec titre et bouton Log In / Log Out ---
col1, col2 = st.columns([6,1])
with col1:
    st.markdown("## ⚙️ DataMécanique")
    st.caption("Maintenance prédictive intelligente")
with col2:
    if "role" in st.session_state:
        logout_button()
    else:
        st.button("🔑 Se connecter", on_click=login_form)

# --- Vérifie login ---
if "role" not in st.session_state:
    login_form()

# --- Affiche le rôle et accès ---
st.info(f"Connecté en tant que **{st.session_state.role}**")

# --- Navigation ---
pg = st.navigation([
    st.Page("log.py", title="📝 Logs"),
    st.Page("mesures_capteurs.py", title="📈 Mesures capteurs"),
    st.Page("historiques.py", title="📊 Historique & risques")
])
pg.run()
