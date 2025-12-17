#!/bin/bash


# Démarrer l'API en arrière-plan et rediriger les logs
python ApiPredictDays.py >> /workspaces/Projet_Collecte_Donn-es_IA-2/api_logs.log 2>&1 &

# Démarrer l'application Streamlit en arrière-plan
streamlit run app/main.py &

