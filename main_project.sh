set -e

echo "Starting application..."

# Lancer l'API en arrière-plan
python ApiPredictDays.py >> ./api_logs.log 2>&1 &

echo "API started in the background."

# Gestion du port Streamlit
if [ -z "$PORT" ]; then
  echo "PORT not set, using default 8501 (local mode)"
  STREAMLIT_PORT=8501
else
  echo "PORT detected ($PORT) (Render mode)"
  STREAMLIT_PORT=$PORT
fi

echo "Starting Streamlit on port $STREAMLIT_PORT"

streamlit run app/main.py \
  --server.port=$STREAMLIT_PORT \
  --server.address=0.0.0.0