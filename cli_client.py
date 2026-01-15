#!/usr/bin/env python3
"""
CLI Client pour l'API de Maintenance Prédictive EnergiTech
Ce client permet d'interagir avec l'API de prédiction de pannes depuis la ligne de commande
"""

import argparse
import requests
import json
import sys
from datetime import datetime, timedelta
from typing import Dict, List

# Configuration de l'API
API_BASE_URL = "http://localhost:5000/api"
DEFAULT_TOKEN = "tech_2024_energitech"

# Couleurs ANSI pour le terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text: str):
    """Affiche un en-tête stylisé"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_success(text: str):
    """Affiche un message de succès"""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_error(text: str):
    """Affiche un message d'erreur"""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def print_warning(text: str):
    """Affiche un message d'avertissement"""
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def print_info(text: str):
    """Affiche un message d'information"""
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")

def get_auth_headers(token: str) -> Dict[str, str]:
    """Retourne les headers d'authentification"""
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def check_health(token: str):
    """Vérifie l'état de santé de l'API"""
    print_header("Vérification de l'état de l'API")
    
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"API Status: {data['status'].upper()}")
            print_info(f"Modèle chargé: {'Oui' if data['model_loaded'] else 'Non'}")
            print_info(f"Version API: {data['api_version']}")
            print_info(f"Version Modèle: {data['model_metadata']['version']}")
            
            print(f"\n{Colors.BOLD}Endpoints disponibles:{Colors.ENDC}")
            for endpoint in data['endpoints_available']:
                print(f"  • {endpoint['method']:6} {endpoint['path']:25} - {endpoint['description']}")
            
            return True
        else:
            print_error(f"L'API a retourné une erreur: {response.status_code}")
            return False
    
    except requests.exceptions.ConnectionError:
        print_error("Impossible de se connecter à l'API. Vérifiez qu'elle est démarrée.")
        return False
    except Exception as e:
        print_error(f"Erreur inattendue: {str(e)}")
        return False

def predict_single(token: str, wind_speed: float, vibration: float, temperature: float, 
                   power_output: float, maintenance_done: int):
    """Fait une prédiction unique"""
    print_header("Prédiction de panne - Analyse unique")
    
    payload = {
        "wind_speed": wind_speed,
        "vibration_level": vibration,
        "temperature": temperature,
        "power_output": power_output,
        "maintenance_done": maintenance_done
    }
    
    print(f"{Colors.BOLD}Données d'entrée:{Colors.ENDC}")
    print(f"  • Vitesse du vent: {wind_speed} m/s")
    print(f"  • Niveau de vibration: {vibration}")
    print(f"  • Température: {temperature} °C")
    print(f"  • Puissance: {power_output} kW")
    print(f"  • Maintenance récente: {'Oui' if maintenance_done == 1 else 'Non'}")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/predict",
            json=payload,
            headers=get_auth_headers(token)
        )
        
        if response.status_code == 200:
            result = response.json()
            prediction = result['prediction']
            
            print(f"\n{Colors.BOLD}Résultat de l'analyse:{Colors.ENDC}")
            
            # Afficher le résultat avec couleur selon le risque
            risk_level = prediction['risk_level']
            probability = prediction['probability_of_failure']
            
            if risk_level == "Élevé":
                color = Colors.FAIL
            elif risk_level == "Moyen":
                color = Colors.WARNING
            else:
                color = Colors.OKGREEN
            
            print(f"{color}  • Niveau de risque: {risk_level}{Colors.ENDC}")
            print(f"  • Probabilité de panne: {probability:.1%}")
            print(f"  • Panne prédite: {'OUI' if prediction['will_fail'] else 'NON'}")
            print(f"  • Confiance: {prediction['confidence']:.1%}")
            print(f"  • ID prédiction: {result['prediction_id']}")
            
            print(f"\n{Colors.BOLD}Recommandations:{Colors.ENDC}")
            for rec in result['recommendations']:
                print(f"  • {rec}")
            
            return True
        elif response.status_code == 401:
            print_error("Authentification échouée. Vérifiez votre token.")
            return False
        else:
            print_error(f"Erreur API: {response.status_code}")
            print(response.json())
            return False
    
    except Exception as e:
        print_error(f"Erreur: {str(e)}")
        return False

def predict_batch(token: str, turbines: List[Dict], show_details: bool = False):
    """Fait des prédictions par lot"""
    print_header("Prédictions par lot")
    
    print_info(f"Analyse de {len(turbines)} turbine(s)...")
    
    payload = {"turbines": turbines}
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/batch-predict",
            json=payload,
            headers=get_auth_headers(token)
        )
        
        if response.status_code == 200:
            result = response.json()
            predictions = result['predictions']
            summary = result['summary']
            
            print_success(f"Prédictions réussies: {summary['successful_predictions']}/{summary['total_turbines']}")
            
            if summary['failed_predictions'] > 0:
                print_warning(f"Échecs: {summary['failed_predictions']}")
                if result.get('errors'):
                    print("\nErreurs rencontrées:")
                    for error in result['errors']:
                        print(f"  • {error}")
            
            # Statistiques globales
            high_risk_count = sum(1 for p in predictions if p['risk_level'] == 'Élevé')
            medium_risk_count = sum(1 for p in predictions if p['risk_level'] == 'Moyen')
            low_risk_count = sum(1 for p in predictions if p['risk_level'] == 'Faible')
            failure_count = sum(1 for p in predictions if p['will_fail'])
            
            avg_probability = sum(p['probability_of_failure'] for p in predictions) / len(predictions) if predictions else 0
            
            print(f"\n{Colors.BOLD}Statistiques:{Colors.ENDC}")
            print(f"  • Probabilité moyenne: {avg_probability:.1%}")
            print(f"  • Turbines à risque élevé: {high_risk_count} ({Colors.FAIL}●{Colors.ENDC})")
            print(f"  • Turbines à risque moyen: {medium_risk_count} ({Colors.WARNING}●{Colors.ENDC})")
            print(f"  • Turbines à risque faible: {low_risk_count} ({Colors.OKGREEN}●{Colors.ENDC})")
            print(f"  • Pannes prédites: {failure_count}")
            
            if show_details:
                print(f"\n{Colors.BOLD}Détails des prédictions:{Colors.ENDC}")
                for pred in predictions:
                    risk = pred['risk_level']
                    if risk == "Élevé":
                        color = Colors.FAIL
                    elif risk == "Moyen":
                        color = Colors.WARNING
                    else:
                        color = Colors.OKGREEN
                    
                    print(f"\n  {color}Turbine: {pred['turbine_id']}{Colors.ENDC}")
                    print(f"    • Risque: {risk} ({pred['probability_of_failure']:.1%})")
                    print(f"    • Panne: {'OUI' if pred['will_fail'] else 'NON'}")
            
            return True
        elif response.status_code == 401:
            print_error("Authentification échouée. Vérifiez votre token.")
            return False
        else:
            print_error(f"Erreur API: {response.status_code}")
            print(response.json())
            return False
    
    except Exception as e:
        print_error(f"Erreur: {str(e)}")
        return False

def predict_7_days(token: str, turbine_id: str, base_params: Dict):
    """Génère et prédit sur 7 jours"""
    print_header(f"Prédictions sur 7 jours - Turbine {turbine_id}")
    
    import random
    turbines = []
    start_date = datetime.now()
    
    for day in range(7):
        day_date = start_date + timedelta(days=day)
        
        # Variation simulée
        turbine_data = {
            "turbine_id": f"{turbine_id}_J{day+1}",
            "wind_speed": max(0, min(50, base_params['wind_speed'] + random.uniform(-2, 2))),
            "vibration_level": max(0, min(10, base_params['vibration_level'] + random.uniform(-0.5, 0.5))),
            "temperature": max(-20, min(60, base_params['temperature'] + random.uniform(-2, 2))),
            "power_output": max(0, min(2000, base_params['power_output'] + random.uniform(-100, 100))),
            "maintenance_done": base_params['maintenance_done']
        }
        turbines.append(turbine_data)
        print_info(f"Jour {day+1} ({day_date.strftime('%d/%m/%Y')}): Données générées")
    
    return predict_batch(token, turbines, show_details=True)

def get_model_info(token: str):
    """Obtient les informations sur le modèle"""
    print_header("Informations sur le modèle")
    
    try:
        response = requests.get(
            f"{API_BASE_URL}/model-info",
            headers=get_auth_headers(token)
        )
        
        if response.status_code == 200:
            info = response.json()
            
            print(f"{Colors.BOLD}Modèle:{Colors.ENDC} {info['model_name']}")
            print(f"{Colors.BOLD}Version:{Colors.ENDC} {info['version']}")
            print(f"{Colors.BOLD}Description:{Colors.ENDC} {info['description']}")
            print(f"{Colors.BOLD}Date d'entraînement:{Colors.ENDC} {info['training_date']}")
            
            print(f"\n{Colors.BOLD}Performance:{Colors.ENDC}")
            for metric, value in info['performance_metrics'].items():
                print(f"  • {metric}: {value}")
            
            print(f"\n{Colors.BOLD}Features d'entrée:{Colors.ENDC}")
            for feature in info['input_features']:
                print(f"  • {feature}")
            
            print(f"\n{Colors.BOLD}Limitations:{Colors.ENDC}")
            for limitation in info['limitations']:
                print(f"  • {limitation}")
            
            return True
        elif response.status_code == 401:
            print_error("Authentification échouée.")
            return False
        else:
            print_error(f"Erreur API: {response.status_code}")
            return False
    
    except Exception as e:
        print_error(f"Erreur: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="CLI Client pour l'API de Maintenance Prédictive EnergiTech",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  
  # Vérifier l'état de l'API
  python cli_client.py health
  
  # Faire une prédiction unique
  python cli_client.py predict --wind-speed 12.5 --vibration 4.2 --temperature 28.0 --power 850 --maintenance 0
  
  # Prédictions sur 7 jours
  python cli_client.py predict-7days --turbine-id WIND-001 --wind-speed 10 --vibration 3 --temperature 25 --power 700 --maintenance 0
  
  # Obtenir les informations du modèle
  python cli_client.py model-info
  
  # Utiliser un token différent
  python cli_client.py predict --token manager_2024_energitech --wind-speed 15 ...
        """
    )
    
    parser.add_argument('command', choices=['health', 'predict', 'predict-7days', 'model-info'],
                       help='Commande à exécuter')
    parser.add_argument('--token', default=DEFAULT_TOKEN, help='Token d\'authentification')
    
    # Arguments pour les prédictions
    parser.add_argument('--wind-speed', type=float, help='Vitesse du vent (m/s)')
    parser.add_argument('--vibration', type=float, help='Niveau de vibration')
    parser.add_argument('--temperature', type=float, help='Température (°C)')
    parser.add_argument('--power', type=float, help='Puissance délivrée (kW)')
    parser.add_argument('--maintenance', type=int, choices=[0, 1], help='Maintenance récente (0/1)')
    parser.add_argument('--turbine-id', default='WIND-001', help='ID de la turbine')
    
    args = parser.parse_args()
    
    # Afficher le banner
    print(f"\n{Colors.OKBLUE}{Colors.BOLD}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║   CLI Client - API Maintenance Prédictive EnergiTech      ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}")
    
    # Exécuter la commande
    if args.command == 'health':
        success = check_health(args.token)
    
    elif args.command == 'predict':
        if not all([args.wind_speed, args.vibration, args.temperature, args.power, args.maintenance is not None]):
            print_error("Tous les paramètres sont requis pour une prédiction.")
            print_info("Utilisez --help pour voir les paramètres requis.")
            sys.exit(1)
        
        success = predict_single(
            args.token, 
            args.wind_speed, 
            args.vibration, 
            args.temperature,
            args.power, 
            args.maintenance
        )
    
    elif args.command == 'predict-7days':
        if not all([args.wind_speed, args.vibration, args.temperature, args.power, args.maintenance is not None]):
            print_error("Tous les paramètres de base sont requis.")
            print_info("Utilisez --help pour voir les paramètres requis.")
            sys.exit(1)
        
        base_params = {
            'wind_speed': args.wind_speed,
            'vibration_level': args.vibration,
            'temperature': args.temperature,
            'power_output': args.power,
            'maintenance_done': args.maintenance
        }
        
        success = predict_7_days(args.token, args.turbine_id, base_params)
    
    elif args.command == 'model-info':
        success = get_model_info(args.token)
    
    # Code de sortie
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
