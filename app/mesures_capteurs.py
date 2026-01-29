import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from auth import require_role

require_role(["technicien", "manager"])

st.header("📈 Mesures des capteurs")

# Charger les données
df = pd.read_csv("df_cleaned.csv")

# Aperçu des données
st.subheader("Aperçu des données")
st.dataframe(df.head(), use_container_width=True)

# Sélection des colonnes numériques
df_numeric = df.select_dtypes(include=["int64", "float64"])

# Statistiques des capteurs
st.subheader("Statistiques des capteurs")

# Vérifier que les colonnes requises existent
required_columns = ['wind_speed', 'temperature', 'vibration_level', 'power_output']
missing_columns = [col for col in required_columns if col not in df_numeric.columns]

if missing_columns:
    st.error(f"Colonnes manquantes dans les données : {', '.join(missing_columns)}")
else:
    # Calculer les statistiques pour chaque capteur
    sensors_data = {
        '💨 Vitesse du vent (m/s)': {
            'column': 'wind_speed',
            'color': '#1f77b4'
        },
        '🌡️ Température (°C)': {
            'column': 'temperature',
            'color': '#ff7f0e'
        },
        '📳 Niveau de vibration': {
            'column': 'vibration_level',
            'color': '#2ca02c'
        },
        '⚡ Production d\'énergie (kW)': {
            'column': 'power_output',
            'color': '#d62728'
        }
    }
    
    # Créer un graphique en barres pour chaque capteur
    for sensor_name, sensor_info in sensors_data.items():
        col_name = sensor_info['column']
        color = sensor_info['color']
        
        # Calculer les statistiques
        min_val = df_numeric[col_name].min()
        avg_val = df_numeric[col_name].mean()
        max_val = df_numeric[col_name].max()
        
        # Créer les données pour le graphique
        stats_df = pd.DataFrame({
            'Statistique': ['Minimum', 'Moyenne', 'Maximum'],
            'Valeur': [min_val, avg_val, max_val],
            'Couleur': ['#90CAF9', color, '#FF6B6B']
        })
        
        # Créer le graphique en barres horizontales avec Altair
        chart = (
            alt.Chart(stats_df)
            .mark_bar()
            .encode(
                x=alt.X('Valeur:Q', title='Valeur', scale=alt.Scale(domain=[0, max(max_val * 1.1, 0.1)])),
                y=alt.Y('Statistique:N', title='', sort=['Minimum', 'Moyenne', 'Maximum']),
                color=alt.Color('Couleur:N', scale=None, legend=None),
                tooltip=[
                    alt.Tooltip('Statistique:N', title='Statistique'),
                    alt.Tooltip('Valeur:Q', title='Valeur', format='.2f')
                ]
            )
            .properties(
                height=150,
                title=sensor_name
            )
        )
        
        # Ajouter les valeurs sur les barres
        text = chart.mark_text(
            align='left',
            baseline='middle',
            dx=5,
            fontSize=14,
            fontWeight='bold'
        ).encode(
            text=alt.Text('Valeur:Q', format='.2f')
        )
        
        final_chart = (chart + text).configure_title(
            fontSize=16,
            anchor='start'
        )
        
        st.altair_chart(final_chart, use_container_width=True)

# Visualisations supplémentaires
st.subheader("Visualisations supplémentaires")

# Configuration pour des graphiques compacts
fig_size = (5, 3)  # Taille compacte des figures

# Création de trois colonnes pour afficher les graphiques côte à côte
col1, col2, col3 = st.columns(3)

# 1. Histogramme pour la distribution de 'wind_speed'
with col1:
    st.write("#### Distribution de la vitesse du vent")
    fig, ax = plt.subplots(figsize=fig_size)
    ax.hist(df['wind_speed'], bins=10, color='skyblue', edgecolor='black', alpha=0.7)
    ax.set_title('Vitesse du vent', fontsize=9)
    ax.set_xlabel('Vitesse', fontsize=7)
    ax.set_ylabel('Fréquence', fontsize=7)
    plt.tight_layout()
    st.pyplot(fig)

# 2. Graphique en barres pour 'maintenance_done'
with col2:
    st.write("#### Maintenance effectuée")
    fig, ax = plt.subplots(figsize=fig_size)
    maintenance_counts = df['maintenance_done'].value_counts()
    ax.bar(maintenance_counts.index, maintenance_counts.values,
           color=['lightgreen', 'salmon'])
    ax.set_title('Maintenance', fontsize=9)
    ax.set_xlabel('Statut', fontsize=7)
    ax.set_ylabel('Occurrences', fontsize=7)
    ax.set_xticks([0, 1])
    plt.tight_layout()
    st.pyplot(fig)

# 3. Graphique en ligne pour 'power_output' au fil du temps (10 premières lignes)
with col3:
    st.write("#### Production d'énergie au fil du temps")
    fig, ax = plt.subplots(figsize=fig_size)
    ax.plot(df.head(10)['date_measure'], df.head(10)['power_output'],
            marker='o', color='green', linestyle='-')
    ax.set_title('Production d\'énergie', fontsize=9)
    ax.set_xlabel('Date', fontsize=7)
    ax.set_ylabel('Énergie', fontsize=7)
    plt.xticks(rotation=45, fontsize=6)
    plt.yticks(fontsize=6)
    plt.tight_layout()
    st.pyplot(fig)
