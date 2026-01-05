import streamlit as st
import pandas as pd
from auth import require_role

require_role(["technicien", "manager"])

st.header("📝 Journaux système")
st.subheader(f"Rôle actuel : {st.session_state.role}")

logs_data = [
    {"date": "2025-12-16 08:00", "machine": "M01", "événement": "Température élevée", "niveau": "alerte"},
    {"date": "2025-12-16 09:30", "machine": "M02", "événement": "Vibration normale", "niveau": "info"},
    {"date": "2025-12-16 10:15", "machine": "M03", "événement": "Panne détectée", "niveau": "critique"},
]

df_logs = pd.DataFrame(logs_data)

if st.session_state.role == "technicien":
    df_logs = df_logs[df_logs["niveau"].isin(["alerte", "critique"])]

st.dataframe(df_logs, use_container_width=True)

if st.session_state.role == "manager":
    st.subheader("📊 Résumé des incidents")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total événements", len(df_logs))
    col2.metric("Alertes", len(df_logs[df_logs["niveau"]=="alerte"]))
    col3.metric("Critiques", len(df_logs[df_logs["niveau"]=="critique"]))

import streamlit as st

# Lire le fichier et permettre son téléchargement
with open("api_logs.log", "rb") as file:  # Notez le mode "rb" pour lire en binaire
    st.download_button(
        label="Télécharger le fichier de log API",
        data=file,
        file_name="api_logs.log",
        mime="text/plain"
    )

st.markdown("---")
st.subheader("📄 Documentation API")
# Permettre le téléchargement de swagger.yaml et afficher un avertissement si absent
try:
    with open("swagger.yaml", "rb") as sw_file:
        st.download_button(
            label="Télécharger la documentation OpenAPI (swagger.yaml)",
            data=sw_file,
            file_name="swagger.yaml",
            mime="text/yaml"
        )
    # Optionnel : afficher un aperçu du YAML lisible
    try:
        with open("swagger.yaml", "r", encoding="utf-8") as sw_text:
            st.code(sw_text.read(), language="yaml")
    except Exception:
        pass
except FileNotFoundError:
    st.warning("Fichier `swagger.yaml` introuvable dans le répertoire racine.")
  

