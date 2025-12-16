import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import altair as alt
from auth import require_role

require_role(["manager"])

st.header("📊 Historique des incidents & pannes")
st.caption("Suivi intelligent des risques de panne")

API_URL_PREDICT = "http://localhost:5000/api/predict"
API_URL_MODEL_INFO = "http://localhost:5000/api/model-info"
API_URL_STATS = "http://localhost:5000/api/stats"

# Configuration des tokens d'authentification
API_TOKENS = {
    'technician_token': 'tech_2024_energitech',
    'manager_token': 'manager_2024_energitech',
    'data_scientist_token': 'ds_2024_energitech'
}

# Fonction pour obtenir les headers d'authentification
def get_auth_headers(token_key):
    return {
        "Authorization": f"Bearer {API_TOKENS.get(token_key, '')}"
    }

# Formulaire prédiction
st.subheader("Nouvelle analyse de risque")
with st.form("prediction_form"):
    col1, col2, col3 = st.columns(3)
    temperature = col1.number_input("🌡️ Température", value=25.0)
    vibration = col2.number_input("📳 Vibration", value=3.2)
    wind_speed = col3.number_input("💨 Vitesse du vent", value=10.5)
    power_output = col1.number_input("⚡ Puissance délivrée (kW)", value=750.0)
    maintenance_done = col2.selectbox("🔧 Maintenance récente", options=[0, 1], format_func=lambda x: "Oui" if x == 1 else "Non")
    submit = st.form_submit_button("🔍 Analyser le risque")

if submit:
    payload = {
        "wind_speed": wind_speed,
        "vibration_level": vibration,
        "temperature": temperature,
        "power_output": power_output,
        "maintenance_done": maintenance_done
    }

    try:
        response = requests.post(API_URL_PREDICT, json=payload, headers=get_auth_headers('manager_token'))

        if response.status_code == 200:
            result = response.json()
            st.success("Analyse terminée avec succès")

            if "history" not in st.session_state:
                st.session_state.history = []

            st.session_state.history.append({
                "date": datetime.now(),
                "temperature": temperature,
                "vibration": vibration,
                "wind_speed": wind_speed,
                "power_output": power_output,
                "maintenance_done": maintenance_done,
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

    wind_chart = alt.Chart(df_reset).mark_line(color="orange").encode(
        x='date:T', y='wind_speed:Q', tooltip=['date:T','wind_speed:Q']
    ).properties(height=200, title="Vitesse du vent")

    power_chart = alt.Chart(df_reset).mark_line(color="purple").encode(
        x='date:T', y='power_output:Q', tooltip=['date:T','power_output:Q']
    ).properties(height=200, title="Puissance délivrée")

    st.altair_chart(prob_chart, use_container_width=True)
    st.altair_chart(temp_chart, use_container_width=True)
    st.altair_chart(vib_chart, use_container_width=True)
    st.altair_chart(wind_chart, use_container_width=True)
    st.altair_chart(power_chart, use_container_width=True)

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

# Informations sur le modèle
st.divider()
st.subheader("📚 Informations sur le modèle")
try:
    response = requests.get(API_URL_MODEL_INFO, headers=get_auth_headers('manager_token'))
    if response.status_code == 200:
        model_info = response.json()
        st.markdown(f"""
        **Modèle :** {model_info['model_name']}
        **Version :** {model_info['version']}
        **Description :** {model_info['description']}
        **Date d'entraînement :** {model_info['training_date']}

        **Performance :**
        - Accuracy : {model_info['performance_metrics']['accuracy']}
        - Précision : {model_info['performance_metrics']['precision']}
        - Recall : {model_info['performance_metrics']['recall']}
        - F1 Score : {model_info['performance_metrics']['f1_score']}

        **Caractéristiques :**
        - {', '.join(model_info['input_features'])}
        """)
    else:
        st.error(f"Erreur lors de la récupération des informations du modèle : {response.status_code}")
except Exception as e:
    st.error(f"Impossible de contacter l'API pour obtenir les informations du modèle : {e}")

# Statistiques
st.divider()
st.subheader("📊 Statistiques d'utilisation")
try:
    response = requests.get(API_URL_STATS, headers=get_auth_headers('manager_token'))
    if response.status_code == 200:
        stats = response.json()
        col1, col2, col3 = st.columns(3)
        col1.metric("Temps de disponibilité", stats['uptime'])
        col2.metric("Requêtes aujourd'hui", stats['model_requests_today'])
        col3.metric("Taux de succès", f"{stats['success_rate'] * 100:.1f}%")
    else:
        st.error(f"Erreur lors de la récupération des statistiques : {response.status_code}")
except Exception as e:
    st.error(f"Impossible de contacter l'API pour obtenir les statistiques : {e}")
