import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import altair as alt
from auth import require_role

# =============================
# CONTRÔLE D'ACCÈS
# =============================
require_role(["manager"])

# =============================
# CONFIG PAGE
# =============================
st.title("📊 Tableau de bord – Suivi intelligent des pannes")
st.caption("Analyse visuelle du risque et aide à la décision")

# =============================
# CONFIG API
# =============================
API_URL_PREDICT = "http://localhost:5000/api/predict"
API_URL_MODEL_INFO = "http://localhost:5000/api/model-info"
API_URL_STATS = "http://localhost:5000/api/stats"

API_TOKENS = {
    "manager_token": "manager_2024_energitech"
}

def get_auth_headers(token_key="manager_token"):
    return {
        "Authorization": f"Bearer {API_TOKENS[token_key]}"
    }

# =============================
# FORMULAIRE D'ANALYSE
# =============================
st.subheader("🔍 Nouvelle analyse de risque")

with st.form("prediction_form"):
    col1, col2, col3 = st.columns(3)

    temperature = col1.number_input("🌡️ Température (°C)", value=25.0)
    vibration = col2.number_input("📳 Vibration", value=3.0)
    wind_speed = col3.number_input("💨 Vitesse du vent (m/s)", value=10.0)
    power_output = col1.number_input("⚡ Puissance délivrée (kW)", value=700.0)
    maintenance_done = col2.selectbox(
        "🔧 Maintenance récente",
        options=[0, 1],
        format_func=lambda x: "Oui" if x == 1 else "Non"
    )

    submit = st.form_submit_button("🔍 Analyser le risque")

if submit:
    payload = {
        "temperature": temperature,
        "vibration_level": vibration,
        "wind_speed": wind_speed,
        "power_output": power_output,
        "maintenance_done": maintenance_done
    }

    try:
        response = requests.post(
            API_URL_PREDICT,
            json=payload,
            headers=get_auth_headers()
        )

        if response.status_code == 200:
            result = response.json()

            if "history" not in st.session_state:
                st.session_state.history = []

            st.session_state.history.append({
                "date": datetime.now(),
                "temperature": float(temperature),
                "vibration": float(vibration),
                "wind_speed": float(wind_speed),
                "power_output": float(power_output),
                "maintenance_done": int(maintenance_done),
                "risk_level": result["prediction"]["risk_level"],
                "probability": float(result["prediction"]["probability_of_failure"])
            })

            st.success("Analyse enregistrée avec succès")
        else:
            st.error(f"Erreur API : {response.status_code}")
    except Exception as e:
        st.error(f"Impossible de contacter l'API : {e}")

# =============================
# TABLEAU DE BORD – RISQUE
# =============================
st.divider()
st.subheader("📈 Synthèse du risque")

if "history" in st.session_state and st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    last_7_days = df[df["date"] >= datetime.now() - timedelta(days=7)].copy()

    def risk_to_band(p):
        if p > 0.7:
            return "Risque élevé"
        elif p > 0.4:
            return "Risque moyen"
        else:
            return "Risque faible"

    last_7_days["risk_band"] = last_7_days["probability"].apply(risk_to_band)

    avg_prob = last_7_days["probability"].mean()
    last_risk = df.iloc[-1]["risk_level"]

    col1, col2, col3 = st.columns(3)
    col1.metric("Risque moyen (7 jours)", f"{avg_prob:.1%}")
    col2.metric("Dernier niveau de risque", last_risk)
    col3.metric("Analyses effectuées", len(df))

    st.subheader("📉 Évolution du risque (7 jours)")

    risk_chart = (
        alt.Chart(last_7_days)
        .mark_line(point=True)
        .encode(
            x=alt.X("date:T", title="Date"),
            y=alt.Y("probability:Q", title="Probabilité de panne", scale=alt.Scale(domain=[0, 1])),
            color=alt.Color(
                "risk_band:N",
                scale=alt.Scale(
                    domain=["Risque faible", "Risque moyen", "Risque élevé"],
                    range=["green", "orange", "red"]
                ),
                title="Niveau de risque"
            ),
            tooltip=[
                alt.Tooltip("date:T", title="Date"),
                alt.Tooltip("probability:Q", title="Probabilité", format=".2%"),
                alt.Tooltip("risk_band:N", title="Risque")
            ]
        )
        .properties(height=350)
    )

    st.altair_chart(risk_chart, use_container_width=True)

    st.subheader("⚙️ Facteurs techniques observés")

    def sensor_chart(field, label):
        return (
            alt.Chart(last_7_days)
            .mark_line(point=True)
            .encode(
                x="date:T",
                y=alt.Y(f"{field}:Q", title=label),
                tooltip=["date:T", f"{field}:Q"]
            )
            .properties(height=200)
        )

    st.altair_chart(sensor_chart("temperature", "Température (°C)"), use_container_width=True)
    st.altair_chart(sensor_chart("vibration", "Vibration"), use_container_width=True)
    st.altair_chart(sensor_chart("wind_speed", "Vitesse du vent (m/s)"), use_container_width=True)
    st.altair_chart(sensor_chart("power_output", "Puissance délivrée (kW)"), use_container_width=True)

    st.subheader("📋 Détail des analyses")
    st.dataframe(last_7_days, use_container_width=True)

else:
    st.info("Aucune analyse enregistrée pour le moment.")

# =============================
# INFORMATIONS SUR LE MODÈLE
# =============================
st.divider()
st.subheader("📚 Informations sur le modèle")

try:
    response = requests.get(API_URL_MODEL_INFO, headers=get_auth_headers("manager_token"))
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

**Caractéristiques d'entrée :**
- {', '.join(model_info['input_features'])}
""")
    else:
        st.error(f"Erreur récupération infos modèle : {response.status_code}")
except Exception as e:
    st.error(f"Impossible de contacter l'API modèle : {e}")

# =============================
# STATISTIQUES D’UTILISATION
# =============================
st.divider()
st.subheader("📊 Statistiques d'utilisation")

try:
    response = requests.get(API_URL_STATS, headers=get_auth_headers("manager_token"))
    if response.status_code == 200:
        stats = response.json()
        col1, col2, col3 = st.columns(3)
        col1.metric("Temps de disponibilité", stats["uptime"])
        col2.metric("Requêtes aujourd'hui", stats["model_requests_today"])
        col3.metric("Taux de succès", f"{stats['success_rate'] * 100:.1f}%")
    else:
        st.error(f"Erreur récupération statistiques : {response.status_code}")
except Exception as e:
    st.error(f"Impossible de contacter l'API statistiques : {e}")
