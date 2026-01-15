#!/usr/bin/env python3
"""
Exemple d'utilisation du CLI Client dans un script Python
Ce script montre comment intégrer le CLI dans un système d'automatisation
"""

import subprocess
import sys
from datetime import datetime

def run_cli_command(command_args):
    """
    Exécute une commande CLI et retourne le résultat
    """
    cmd = ['python', 'cli_client.py'] + command_args
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def check_api_health():
    """
    Vérifie si l'API est disponible
    """
    print("=" * 60)
    print("Vérification de l'état de l'API...")
    print("=" * 60)
    
    returncode, stdout, stderr = run_cli_command(['health'])
    
    if returncode == 0:
        print("✓ API opérationnelle")
        return True
    else:
        print("✗ API non disponible")
        print(stderr)
        return False

def analyze_turbine(turbine_id, parameters):
    """
    Analyse une turbine avec les paramètres donnés
    """
    print(f"\n{'=' * 60}")
    print(f"Analyse de la turbine {turbine_id}")
    print("=" * 60)
    
    command_args = [
        'predict',
        '--wind-speed', str(parameters['wind_speed']),
        '--vibration', str(parameters['vibration']),
        '--temperature', str(parameters['temperature']),
        '--power', str(parameters['power']),
        '--maintenance', str(parameters['maintenance'])
    ]
    
    returncode, stdout, stderr = run_cli_command(command_args)
    
    if returncode == 0:
        print(stdout)
        # Analyser la sortie pour extraire le niveau de risque
        if "Risque: Élevé" in stdout:
            return "HIGH_RISK"
        elif "Risque: Moyen" in stdout:
            return "MEDIUM_RISK"
        else:
            return "LOW_RISK"
    else:
        print(f"✗ Erreur lors de l'analyse: {stderr}")
        return "ERROR"

def analyze_turbine_7days(turbine_id, base_parameters):
    """
    Analyse une turbine sur 7 jours
    """
    print(f"\n{'=' * 60}")
    print(f"Analyse 7 jours de la turbine {turbine_id}")
    print("=" * 60)
    
    command_args = [
        'predict-7days',
        '--turbine-id', turbine_id,
        '--wind-speed', str(base_parameters['wind_speed']),
        '--vibration', str(base_parameters['vibration']),
        '--temperature', str(base_parameters['temperature']),
        '--power', str(base_parameters['power']),
        '--maintenance', str(base_parameters['maintenance'])
    ]
    
    returncode, stdout, stderr = run_cli_command(command_args)
    
    if returncode == 0:
        print(stdout)
        # Compter les turbines à risque élevé
        high_risk_count = stdout.count("Risque: Élevé")
        return high_risk_count
    else:
        print(f"✗ Erreur lors de l'analyse: {stderr}")
        return -1

def main():
    """
    Fonction principale - exemple d'utilisation
    """
    print("\n" + "=" * 60)
    print("Script d'automatisation - Surveillance des turbines")
    print(f"Exécution le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 1. Vérifier que l'API fonctionne
    if not check_api_health():
        print("\n⚠ Impossible de continuer sans API fonctionnelle")
        sys.exit(1)
    
    # 2. Définir les turbines à surveiller
    turbines = [
        {
            'id': 'WIND-001',
            'parameters': {
                'wind_speed': 12.5,
                'vibration': 4.2,
                'temperature': 28.0,
                'power': 850,
                'maintenance': 0
            }
        },
        {
            'id': 'WIND-002',
            'parameters': {
                'wind_speed': 15.0,
                'vibration': 5.5,
                'temperature': 32.0,
                'power': 1200,
                'maintenance': 0
            }
        },
        {
            'id': 'WIND-003',
            'parameters': {
                'wind_speed': 8.0,
                'vibration': 2.5,
                'temperature': 22.0,
                'power': 600,
                'maintenance': 1
            }
        }
    ]
    
    # 3. Analyser chaque turbine
    results = {}
    for turbine in turbines:
        risk_level = analyze_turbine(turbine['id'], turbine['parameters'])
        results[turbine['id']] = risk_level
    
    # 4. Générer un rapport de synthèse
    print("\n" + "=" * 60)
    print("RAPPORT DE SYNTHÈSE")
    print("=" * 60)
    
    high_risk_turbines = [tid for tid, level in results.items() if level == "HIGH_RISK"]
    medium_risk_turbines = [tid for tid, level in results.items() if level == "MEDIUM_RISK"]
    low_risk_turbines = [tid for tid, level in results.items() if level == "LOW_RISK"]
    
    print(f"\nTurbines analysées: {len(turbines)}")
    print(f"  • Risque élevé: {len(high_risk_turbines)} - {high_risk_turbines}")
    print(f"  • Risque moyen: {len(medium_risk_turbines)} - {medium_risk_turbines}")
    print(f"  • Risque faible: {len(low_risk_turbines)} - {low_risk_turbines}")
    
    # 5. Actions à prendre
    if high_risk_turbines:
        print("\n⚠ ALERTE: Interventions urgentes requises!")
        print("Turbines à inspecter immédiatement:")
        for tid in high_risk_turbines:
            print(f"  • {tid}")
            # Ici on pourrait:
            # - Envoyer un email
            # - Créer un ticket
            # - Déclencher une alerte
    
    if medium_risk_turbines:
        print("\n⚠ Attention: Surveillance renforcée recommandée")
        print("Turbines à planifier pour maintenance préventive:")
        for tid in medium_risk_turbines:
            print(f"  • {tid}")
    
    # 6. Exemple d'analyse 7 jours pour les turbines à risque
    if high_risk_turbines or medium_risk_turbines:
        print("\n" + "=" * 60)
        print("ANALYSE DÉTAILLÉE SUR 7 JOURS")
        print("=" * 60)
        
        for turbine in turbines:
            if turbine['id'] in high_risk_turbines or turbine['id'] in medium_risk_turbines:
                high_risk_days = analyze_turbine_7days(turbine['id'], turbine['parameters'])
                if high_risk_days > 0:
                    print(f"\n⚠ {turbine['id']}: {high_risk_days} jour(s) à risque élevé détecté(s)")
    
    print("\n" + "=" * 60)
    print("Fin de l'analyse")
    print("=" * 60)

if __name__ == "__main__":
    main()
