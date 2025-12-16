import streamlit as st

USERS = {
    "technicien": {"password": "tech123", "role": "technicien"},
    "manager": {"password": "manager123", "role": "manager"}
}

def login_form():
    """Affiche le formulaire login si non connecté"""
    if "role" not in st.session_state:
        with st.form("login_form"):
            username = st.text_input("Nom d'utilisateur")
            password = st.text_input("Mot de passe", type="password")
            login_btn = st.form_submit_button("Se connecter")
        if login_btn:
            if username in USERS and password == USERS[username]["password"]:
                st.session_state.role = USERS[username]["role"]
                st.success(f"Connecté en tant que {st.session_state.role}")
                st.experimental_rerun()
            else:
                st.error("Identifiant ou mot de passe incorrect")
        st.stop()

def logout_button():
    """Affiche un bouton logout"""
    if "role" in st.session_state:
        if st.button("🔓 Déconnexion"):
            del st.session_state["role"]
            st.success("Déconnecté avec succès")
            st.experimental_rerun()

def require_role(roles):
    """Vérifie que l'utilisateur a le bon rôle"""
    if "role" not in st.session_state:
        login_form()
    elif st.session_state.role not in roles:
        st.error("🚫 Vous n'êtes pas autorisé à accéder à cette page")
        st.stop()
