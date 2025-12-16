import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import altair as alt
from auth import require_role

require_role(["manager"])

st.header("📊 Historique des incidents & pannes")
st.caption("Suivi intelligent des risques de panne")

API_URL = "http://localhost:5000/api/predict"

# Formulaire prédiction
st.subheader("Nouvelle analyse de risque")
with st.form("prediction_form"):
    col1, col2, col3 = st.columns(3)
    temperature = col1.number_input("🌡️ Température", value=75.0)
    vibration = col2.number_input("📳 Vibration", value=0.4)
    pressure = col3.number_input("💨 Pression", value=1.2)
    submit = st.form_submit_button("🔍 Analyser le risque")

if submit:
    payload = {"temperature": temperature, "vibration": vibration, "pressure": pressure}
    try:
        response = requests.post(API_URL, json=payload, auth=("admin","password"))
        if response.status_code == 200:
            result = response.json()
            st.success("Analyse terminée avec succès")
            if "history" not in st.session_state:
                st.session_state.history = []
            st.session_state.history.append({
                "date": datetime.now(),
                "temperature": temperature,
                "vibration": vibration,
                "pressure": pressure,
                "risk_level": result["prediction"]["risk_level"],
                "probability": result["prediction"]["probability_of_failure"]
            })
        else:
            st.error(f"Erreur API : {response.status_code}")
            st.json(response.json())
    except Exception as e:
        st.error(f"Impossible de contacter l'API : {e}")

# Dashboard premium
st.divider()
st.subheader("📈 Suivi du risque de panne")
if "history" in st.session_state and st.session_state.history:
    df = pd.DataFrame(st.session_state.history).sort_values("date").set_index("date")
    last = df.iloc[-1]
    col1, col2, col3 = st.columns(3)
    col1.metric("Dernière probabilité", f"{last['probability']:.2%}")
    col2.metric("Niveau de risque", last["risk_level"])
    col3.metric("Analyses effectuées", len(df))
    df_reset = df.reset_index()

    prob_chart = alt.Chart(df_reset).mark_line(color="red", point=True).encode(
        x='date:T', y='probability:Q', tooltip=['date:T','probability:Q','risk_level:N']
    ).properties(height=350, title="Probabilité de panne")

    temp_chart = alt.Chart(df_reset).mark_line(color="blue").encode(
        x='date:T', y='temperature:Q', tooltip=['date:T','temperature:Q']
    ).properties(height=200, title="Température")

    vib_chart = alt.Chart(df_reset).mark_line(color="green").encode(
        x='date:T', y='vibration:Q', tooltip=['date:T','vibration:Q']
    ).properties(height=200, title="Vibration")

    pressure_chart = alt.Chart(df_reset).mark_line(color="orange").encode(
        x='date:T', y='pressure:Q', tooltip=['date:T','pressure:Q']
    ).properties(height=200, title="Pression")

    st.altair_chart(prob_chart, use_container_width=True)
    st.altair_chart(temp_chart, use_container_width=True)
    st.altair_chart(vib_chart, use_container_width=True)
    st.altair_chart(pressure_chart, use_container_width=True)

    st.markdown("""
    **Seuils :**
    - 🟢 Faible : < 40 %
    - 🟠 Moyen : 40 – 70 %
    - 🔴 Élevé : > 70 %
    """)

    st.subheader("📋 Détail des analyses")
    st.dataframe(df, use_container_width=True)
else:
    st.info("Aucune analyse enregistrée pour le moment")
