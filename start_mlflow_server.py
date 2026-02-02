#!/usr/bin/env python
"""
Script de démarrage du serveur MLflow
Exécutez : python start_mlflow_server.py
"""

import subprocess
import sys
import os
import time
import signal

def start_mlflow_server(
    backend_uri="file:///content/mlruns",
    host="0.0.0.0",
    port=5000,
    verbose=True
):
    """
    Démarre le serveur MLflow UI
    
    Args:
        backend_uri (str): URI du backend de suivi
        host (str): Hôte du serveur
        port (int): Port du serveur
        verbose (bool): Afficher les logs
    """
    
    # S'assurer que le répertoire existe
    backend_path = backend_uri.replace("file://", "")
    os.makedirs(backend_path, exist_ok=True)
    
    print("\n" + "="*70)
    print("🚀 DÉMARRAGE DU SERVEUR MLFLOW")
    print("="*70)
    print(f"\n📊 Configuration :")
    print(f"   - Backend URI : {backend_uri}")
    print(f"   - Hôte : {host}")
    print(f"   - Port : {port}")
    print(f"   - Répertoire : {backend_path}")
    
    # Arrêter les serveurs existants
    print("\n🛑 Arrêt des serveurs MLflow existants...")
    os.system("pkill -f 'mlflow ui' 2>/dev/null || true")
    time.sleep(1)
    
    try:
        # Lancer le serveur
        print("\n⏳ Démarrage du serveur...")
        
        stdout_file = subprocess.DEVNULL if not verbose else None
        stderr_file = subprocess.DEVNULL if not verbose else None
        
        process = subprocess.Popen(
            [
                "mlflow", "ui",
                "--backend-store-uri", backend_uri,
                "--host", host,
                "--port", str(port)
            ],
            stdout=stdout_file,
            stderr=stderr_file
        )
        
        time.sleep(3)
        
        print("\n✅ SERVEUR MLFLOW ACTIF!")
        print("\n" + "="*70)
        print("🌐 ACCÈS À L'INTERFACE :")
        print("="*70)
        print(f"\nURL locale : http://{host}:{port}")
        print(f"URL localhost : http://localhost:{port}")
        print("\n" + "="*70)
        
        print("\n💡 Conseils d'utilisation :")
        print("   1. Ouvrez http://localhost:5000 dans votre navigateur")
        print("   2. Explorez les expériences et les runs")
        print("   3. Comparez les modèles et les métriques")
        print("   4. Téléchargez les artifacts et les modèles")
        
        print("\n🔐 Pour arrêter le serveur :")
        print("   - Appuyez sur Ctrl+C (vous serez ramené au terminal)")
        print("   - Le processus en arrière-plan continuera à s'exécuter")
        
        print("\n" + "="*70)
        
        # Garder le serveur actif
        process.wait()
        
    except KeyboardInterrupt:
        print("\n\n⏸️  Arrêt du serveur demandé...")
        process.terminate()
        time.sleep(1)
        if process.poll() is None:
            process.kill()
        print("✅ Serveur arrêté")
        
    except FileNotFoundError:
        print("\n❌ ERREUR : MLflow n'est pas installé!")
        print("\nPour installer MLflow, exécutez :")
        print("   pip install mlflow")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ ERREUR : {e}")
        sys.exit(1)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Démarrer le serveur MLflow pour le projet Turbine Prediction"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Port du serveur MLflow (défaut: 5000)"
    )
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Hôte du serveur (défaut: 0.0.0.0)"
    )
    parser.add_argument(
        "--backend",
        type=str,
        default="file:///content/mlruns",
        help="URI du backend MLflow (défaut: file:///content/mlruns)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Afficher les logs du serveur"
    )
    
    args = parser.parse_args()
    
    start_mlflow_server(
        backend_uri=args.backend,
        host=args.host,
        port=args.port,
        verbose=args.verbose
    )
