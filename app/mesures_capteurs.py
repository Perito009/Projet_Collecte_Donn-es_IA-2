import streamlit as st
import pandas as pd
from auth import require_role

require_role(["technicien", "manager"])

st.header("📈 Mesures des capteurs")

df = pd.read_csv("df_cleaned.csv")

st.subheader("Aperçu des données")
st.dataframe(df.head(), use_container_width=True)

df_numeric = df.select_dtypes(include=["int64", "float64"])

st.subheader("Évolution des variables numériques")
st.line_chart(df_numeric, height=350, use_container_width=True)
