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

# Évolution des variables numériques
st.subheader("Évolution des variables numériques")

# Ajouter un index pour visualisation temporelle
df_indexed = df_numeric.reset_index()
df_indexed = df_indexed.rename(columns={'index': 'measurement_id'})

# Vérifier que les colonnes requises existent
required_columns = ['wind_speed', 'temperature', 'vibration_level', 'power_output']
missing_columns = [col for col in required_columns if col not in df_indexed.columns]

if missing_columns:
    st.error(f"Colonnes manquantes dans les données : {', '.join(missing_columns)}")
else:
    # Limiter les données si nécessaire (Altair recommande max 5000 lignes)
    if len(df_indexed) > 5000:
        st.info(f"Affichage des 5000 premières mesures sur {len(df_indexed)} disponibles.")
        df_indexed = df_indexed.head(5000)
    
    # Fonction pour créer un graphique interactif avec Altair
    def create_interactive_chart(data, y_field, y_title, color='steelblue'):
        chart = (
            alt.Chart(data)
            .mark_line(point=True)
            .encode(
                x=alt.X('measurement_id:Q', title='Mesure', axis=alt.Axis(format='d')),
                y=alt.Y(f'{y_field}:Q', title=y_title),
                tooltip=[
                    alt.Tooltip('measurement_id:Q', title='Mesure'),
                    alt.Tooltip(f'{y_field}:Q', title=y_title, format='.2f')
                ]
            )
            .properties(
                height=250
            )
            .configure_mark(
                color=color,
                opacity=0.8
            )
            .interactive()
        )
        return chart
    
    # Créer 2 colonnes pour diviser les graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 💨 Vitesse du vent")
        wind_chart = create_interactive_chart(df_indexed, 'wind_speed', 'Vitesse du vent (m/s)', '#1f77b4')
        st.altair_chart(wind_chart, use_container_width=True)
        
        st.markdown("##### 🌡️ Température")
        temp_chart = create_interactive_chart(df_indexed, 'temperature', 'Température (°C)', '#ff7f0e')
        st.altair_chart(temp_chart, use_container_width=True)
    
    with col2:
        st.markdown("##### 📳 Niveau de vibration")
        vib_chart = create_interactive_chart(df_indexed, 'vibration_level', 'Niveau de vibration', '#2ca02c')
        st.altair_chart(vib_chart, use_container_width=True)
        
        st.markdown("##### ⚡ Production d'énergie")
        power_chart = create_interactive_chart(df_indexed, 'power_output', 'Production d\'énergie (kW)', '#d62728')
        st.altair_chart(power_chart, use_container_width=True)

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
