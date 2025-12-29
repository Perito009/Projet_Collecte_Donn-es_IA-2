set -e

echo "Starting application..."

# Lancer l'API en arrière-plan
python ApiPredictDays.py >> /workspaces/Projet_Collecte_Donn-es_IA-2/api_logs.log 2>&1 &

echo "API started in the background."
# Lancer Streamlit (process principal)
streamlit run app/main.py