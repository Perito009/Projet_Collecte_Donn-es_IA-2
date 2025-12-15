import streamlit as st
import pandas as pd

st.title("Notre Application de Panne dans les 7 jours")

df = pd.read_csv("energiTech_maintenance_sample.csv")

st.subheader("Aperçu des données")
st.dataframe(df.head())

df_numeric = df.select_dtypes(include=["int64", "float64"])

st.subheader("Évolution des variables numériques")
st.line_chart(df_numeric)