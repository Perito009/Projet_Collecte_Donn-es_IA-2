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
