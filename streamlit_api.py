import streamlit as st
import pandas as pd

st.write("NOtre Application de Panne dans les 7 jours")


df= pd.read_csv(energiTech_maintenance_sample.csv)
st.line_chart(df)

