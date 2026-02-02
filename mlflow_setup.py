#!/usr/bin/env python
"""
Configuration MLflow centralisée pour le projet Turbine Prediction
Ce script configure et initialise MLflow pour toutes les expériences
"""

import os
import mlflow
from mlflow.tracking import MlflowClient
import subprocess
import time
import sys

class MLflowSetup:
    """Classe pour initialiser et gérer MLflow"""
    
    def __init__(self, backend_uri="file:///content/mlruns"):
        """
        Initialise la configuration MLflow
        
        Args:
            backend_uri (str): URI du backend de suivi MLflow
        """
        self.backend_uri = backend_uri
        self.mlflow_dir = backend_uri.replace("file://", "")
        
    def create_backend_directory(self):
        """Crée le répertoire du backend s'il n'existe pas"""
        os.makedirs(self.mlflow_dir, exist_ok=True)
        print(f"✓ Répertoire MLflow créé/vérifié : {self.mlflow_dir}")
        
    def setup_tracking(self):
        """Configure MLflow avec le backend"""
        mlflow.set_tracking_uri(self.backend_uri)
        print(f"✓ URI de suivi MLflow configuré : {self.backend_uri}")
        
    def create_experiments(self):
        """Crée les expériences principales"""
        experiments_config = {
            "Turbine_Failure_Prediction_Classification": {
                "description": "Modèle A : Prédiction de pannes (Classification)",
                "tags": {"model_type": "classification", "target": "failure_within_7d"}
            },
            "Turbine_Time_to_Failure_Prediction_Regression": {
                "description": "Modèle B : Prédiction du temps jusqu'à panne (Régression)",
                "tags": {"model_type": "regression", "target": "time_to_failure_days"}
            },
        }
        
        client = MlflowClient(self.backend_uri)
        
        for exp_name, exp_config in experiments_config.items():
            try:
                exp = client.get_experiment_by_name(exp_name)
                if exp is None:
                    exp_id = client.create_experiment(
                        name=exp_name,
                        tags=exp_config.get("tags", {})
                    )
                    print(f"✓ Expérience créée : {exp_name} (ID: {exp_id})")
                else:
                    print(f"✓ Expérience existante : {exp_name} (ID: {exp.experiment_id})")
            except Exception as e:
                print(f"⚠️ Erreur lors de la création de {exp_name}: {e}")
                
    def start_ui_server(self, host="0.0.0.0", port=5000):
        """Démarre le serveur MLflow UI"""
        # Arrêter les serveurs existants
        os.system("pkill -f 'mlflow ui' 2>/dev/null || true")
        time.sleep(1)
        
        print(f"\n📊 Démarrage du serveur MLflow UI...")
        print(f"   Adresse : {host}:{port}")
        
        try:
            subprocess.Popen(
                ["mlflow", "ui", 
                 "--backend-store-uri", self.backend_uri,
                 "--host", host,
                 "--port", str(port)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            time.sleep(2)
            print(f"✓ Serveur MLflow UI lancé avec succès!")
            print(f"\n🌐 Accès : http://localhost:{port}")
            return True
        except Exception as e:
            print(f"❌ Erreur au démarrage du serveur : {e}")
            return False
            
    def get_experiment_info(self):
        """Affiche les informations sur les expériences existantes"""
        client = MlflowClient(self.backend_uri)
        experiments = client.search_experiments()
        
        print("\n" + "="*70)
        print("📋 EXPÉRIENCES MLFLOW")
        print("="*70)
        
        for exp in experiments:
            if exp.name != "Default":
                runs = client.search_runs(experiment_ids=[exp.experiment_id])
                print(f"\n📁 {exp.name}")
                print(f"   ID : {exp.experiment_id}")
                print(f"   Nombre de runs : {len(runs)}")
                
                if runs:
                    latest_run = runs[0]
                    print(f"   Dernier run : {latest_run.info.run_name}")
                    print(f"   Status : {latest_run.info.status}")
                    
    def full_setup(self, start_server=True):
        """Effectue la configuration complète"""
        print("\n" + "="*70)
        print("🚀 CONFIGURATION MLFLOW")
        print("="*70 + "\n")
        
        self.create_backend_directory()
        self.setup_tracking()
        self.create_experiments()
        
        if start_server:
            if not self.start_ui_server():
                print("\n⚠️ Le serveur MLflow n'a pas pu être lancé.")
                print("   Vous pouvez le démarrer manuellement avec :")
                print(f"   mlflow ui --backend-store-uri {self.backend_uri} --port 5000")
        
        self.get_experiment_info()
        
        print("\n" + "="*70)
        print("✅ CONFIGURATION TERMINÉE")
        print("="*70)


def main():
    """Fonction principale"""
    # Configuration par défaut
    backend_uri = "file:///content/mlruns"
    
    # Créer une instance de MLflowSetup
    setup = MLflowSetup(backend_uri=backend_uri)
    
    # Effectuer la configuration complète
    setup.full_setup(start_server=True)


if __name__ == "__main__":
    main()
