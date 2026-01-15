import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import altair as alt
import random
from auth import require_role

# =============================
# CONTRÔLE D'ACCÈS
# =============================
require_role(["manager", "technicien"])

# =============================
# CONFIG PAGE
# =============================
st.title("🔮 Prédictions par lot - 7 jours")
st.caption("Analyse des risques de panne pour les 7 prochains jours")

# =============================
# CONFIG API
# =============================
API_URL_BATCH = "http://localhost:5000/api/batch-predict"

API_TOKENS = {
    "manager_token": "manager_2024_energitech",
    "technician_token": "tech_2024_energitech"
}

def get_auth_headers(token_key="manager_token"):
    return {
        "Authorization": f"Bearer {API_TOKENS[token_key]}"
    }

# =============================
# GÉNÉRATION DE DONNÉES POUR 7 JOURS
# =============================
st.subheader("📊 Configuration des prédictions")

with st.form("batch_prediction_form"):
    st.markdown("### Données de base de l'éolienne")
    
    col1, col2, col3 = st.columns(3)
    
    base_temperature = col1.number_input("🌡️ Température de base (°C)", value=25.0, min_value=-20.0, max_value=60.0)
    base_vibration = col2.number_input("📳 Niveau de vibration de base", value=3.0, min_value=0.0, max_value=10.0)
    base_wind_speed = col3.number_input("💨 Vitesse du vent de base (m/s)", value=10.0, min_value=0.0, max_value=50.0)
    base_power_output = col1.number_input("⚡ Puissance de base (kW)", value=700.0, min_value=0.0, max_value=2000.0)
    base_maintenance = col2.selectbox(
        "🔧 Maintenance récente",
        options=[0, 1],
        format_func=lambda x: "Oui" if x == 1 else "Non"
    )
    
    st.markdown("### Options de variation")
    st.caption("Les données varieront légèrement chaque jour pour simuler des conditions réelles")
    
    col1, col2 = st.columns(2)
    temp_variation = col1.slider("Variation de température (±°C)", 0.0, 10.0, 2.0)
    vibration_variation = col2.slider("Variation de vibration (±)", 0.0, 2.0, 0.5)
    
    turbine_id = st.text_input("🏷️ ID de l'éolienne", value="WIND-001")
    
    submit = st.form_submit_button("🔮 Générer les prédictions sur 7 jours")

if submit:
    st.info("Génération des prédictions pour les 7 prochains jours...")
    
    # Générer les données pour 7 jours
    turbines_data = []
    start_date = datetime.now()
    
    for day in range(7):
        day_date = start_date + timedelta(days=day)
        
        # Variation simulée des paramètres
        temp_offset = random.uniform(-temp_variation, temp_variation)
        vib_offset = random.uniform(-vibration_variation, vibration_variation)
        wind_offset = random.uniform(-2, 2)
        power_offset = random.uniform(-100, 100)
        
        turbine_data = {
            "turbine_id": f"{turbine_id}_day{day+1}",
            "date": day_date.strftime("%Y-%m-%d"),
            "wind_speed": max(0, min(50, base_wind_speed + wind_offset)),
            "vibration_level": max(0, min(10, base_vibration + vib_offset)),
            "temperature": max(-20, min(60, base_temperature + temp_offset)),
            "power_output": max(0, min(2000, base_power_output + power_offset)),
            "maintenance_done": base_maintenance
        }
        turbines_data.append(turbine_data)
    
    # Préparer la payload pour l'API
    payload = {
        "turbines": turbines_data
    }
    
    try:
        # Faire l'appel API
        response = requests.post(
            API_URL_BATCH,
            json=payload,
            headers=get_auth_headers("manager_token")
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # Sauvegarder dans la session
            st.session_state.batch_predictions = result
            st.session_state.turbines_input = turbines_data
            
            st.success(f"✅ Prédictions générées avec succès pour {len(result['predictions'])} jours!")
            
            # Afficher le résumé
            summary = result['summary']
            col1, col2, col3 = st.columns(3)
            col1.metric("Total de jours analysés", summary['total_turbines'])
            col2.metric("Prédictions réussies", summary['successful_predictions'])
            col3.metric("Échecs", summary['failed_predictions'])
            
        else:
            st.error(f"❌ Erreur API : {response.status_code}")
            st.json(response.json())
    
    except Exception as e:
        st.error(f"❌ Impossible de contacter l'API : {e}")

# =============================
# AFFICHAGE DES RÉSULTATS
# =============================
if "batch_predictions" in st.session_state and st.session_state.batch_predictions:
    st.divider()
    st.subheader("📈 Résultats des prédictions sur 7 jours")
    
    predictions = st.session_state.batch_predictions['predictions']
    input_data = st.session_state.turbines_input
    
    # Créer un DataFrame combiné
    df_results = pd.DataFrame(predictions)
    df_input = pd.DataFrame(input_data)
    
    # Fusionner les données
    df_results['date'] = df_input['date']
    df_results['temperature'] = df_input['temperature']
    df_results['vibration'] = df_input['vibration_level']
    df_results['wind_speed'] = df_input['wind_speed']
    df_results['power_output'] = df_input['power_output']
    
    # Ajouter une colonne de risque numérique pour le graphique
    def risk_to_num(risk):
        if risk == "Élevé":
            return 3
        elif risk == "Moyen":
            return 2
        else:
            return 1
    
    df_results['risk_num'] = df_results['risk_level'].apply(risk_to_num)
    
    # Graphique d'évolution du risque
    st.markdown("### 📊 Évolution du risque sur 7 jours")
    
    risk_chart = (
        alt.Chart(df_results)
        .mark_line(point=True, size=3)
        .encode(
            x=alt.X("date:T", title="Date", axis=alt.Axis(format="%d/%m")),
            y=alt.Y("probability_of_failure:Q", title="Probabilité de panne", scale=alt.Scale(domain=[0, 1])),
            color=alt.Color(
                "risk_level:N",
                scale=alt.Scale(
                    domain=["Faible", "Moyen", "Élevé"],
                    range=["green", "orange", "red"]
                ),
                title="Niveau de risque"
            ),
            tooltip=[
                alt.Tooltip("date:T", title="Date", format="%d/%m/%Y"),
                alt.Tooltip("probability_of_failure:Q", title="Probabilité", format=".2%"),
                alt.Tooltip("risk_level:N", title="Risque"),
                alt.Tooltip("temperature:Q", title="Température (°C)", format=".1f"),
                alt.Tooltip("vibration:Q", title="Vibration", format=".1f")
            ]
        )
        .properties(height=400)
    )
    
    st.altair_chart(risk_chart, use_container_width=True)
    
    # Statistiques globales
    st.markdown("### 📊 Statistiques sur la période")
    col1, col2, col3, col4 = st.columns(4)
    
    avg_probability = df_results['probability_of_failure'].mean()
    max_probability = df_results['probability_of_failure'].max()
    high_risk_days = len(df_results[df_results['risk_level'] == 'Élevé'])
    failures_predicted = len(df_results[df_results['will_fail'] == True])
    
    col1.metric("Probabilité moyenne", f"{avg_probability:.1%}")
    col2.metric("Probabilité maximale", f"{max_probability:.1%}")
    col3.metric("Jours à risque élevé", high_risk_days)
    col4.metric("Pannes prédites", failures_predicted)
    
    # Alertes
    if high_risk_days > 0:
        st.warning(f"⚠️ **Attention:** {high_risk_days} jour(s) présentent un risque élevé de panne!")
        high_risk_dates = df_results[df_results['risk_level'] == 'Élevé']['date'].tolist()
        st.markdown("**Dates à surveiller:** " + ", ".join(high_risk_dates))
    
    if failures_predicted > 0:
        st.error(f"🚨 **Alerte:** {failures_predicted} panne(s) probable(s) dans les 7 prochains jours!")
    else:
        st.success("✅ Aucune panne probable dans les 7 prochains jours")
    
    # Recommandations basées sur l'analyse
    st.markdown("### 💡 Recommandations")
    
    if max_probability >= 0.7:
        st.markdown("""
        - 🔴 **Intervention urgente recommandée** dans les 48h
        - Vérifier les composants critiques (vibrations élevées détectées)
        - Préparer les pièces de rechange
        - Planifier une équipe d'intervention
        """)
    elif max_probability >= 0.4:
        st.markdown("""
        - 🟠 **Surveillance renforcée recommandée**
        - Planifier une intervention préventive dans les 7 jours
        - Vérifier les historiques de maintenance
        - Préparer les équipements de diagnostic
        """)
    else:
        st.markdown("""
        - 🟢 **Situation nominale**
        - Maintenir la surveillance standard
        - Continuer les maintenances préventives programmées
        """)
    
    # Tableau détaillé
    st.markdown("### 📋 Détail des prédictions")
    
    # Formater le DataFrame pour l'affichage
    display_df = df_results[['date', 'turbine_id', 'temperature', 'vibration', 'wind_speed', 
                             'power_output', 'probability_of_failure', 'risk_level', 'will_fail']].copy()
    
    display_df.columns = ['Date', 'ID Turbine', 'Temp (°C)', 'Vibration', 'Vent (m/s)', 
                          'Puissance (kW)', 'Probabilité', 'Niveau de risque', 'Panne prédite']
    
    # Styler le tableau
    def color_risk(val):
        if val == 'Élevé':
            return 'background-color: #ffcccc'
        elif val == 'Moyen':
            return 'background-color: #fff4cc'
        else:
            return 'background-color: #ccffcc'
    
    styled_df = display_df.style.applymap(color_risk, subset=['Niveau de risque'])
    st.dataframe(styled_df, use_container_width=True)
    
    # Option d'export
    st.markdown("### 💾 Export des données")
    csv = display_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Télécharger les résultats (CSV)",
        data=csv,
        file_name=f"predictions_7jours_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

else:
    st.info("👆 Utilisez le formulaire ci-dessus pour générer des prédictions sur 7 jours")

# =============================
# INFORMATIONS
# =============================
st.divider()
st.markdown("### ℹ️ À propos")
st.markdown("""
Cette page permet de générer des prédictions de risque de panne sur les 7 prochains jours 
pour une éolienne donnée. Les données varient légèrement chaque jour pour simuler 
des conditions réelles.

**Comment utiliser:**
1. Entrez les paramètres de base de l'éolienne
2. Ajustez les variations souhaitées
3. Cliquez sur "Générer les prédictions"
4. Analysez les graphiques et recommandations
5. Exportez les résultats si nécessaire
""")
