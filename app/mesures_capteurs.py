import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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
st.line_chart(df_numeric, height=350, use_container_width=True)

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
