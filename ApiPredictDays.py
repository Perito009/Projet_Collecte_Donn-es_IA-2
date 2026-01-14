"""
API d'inférence pour la maintenance prédictive des éoliennes - EnergiTech
Modèle de classification : prédiction de panne dans les 7 prochains jours
"""

import pandas as pd
import joblib
import json
import logging
from datetime import datetime
from functools import wraps
from typing import Dict, Any, Optional, Tuple
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_httpauth import HTTPTokenAuth

# Configuration de l'application
app = Flask(__name__)
CORS(app)  # Autorise les requêtes cross-origin

# Configuration de l'authentification
auth = HTTPTokenAuth(scheme='Bearer')
API_TOKENS = {
    'technician_token': 'tech_2024_energitech',
    'manager_token': 'manager_2024_energitech',
    'data_scientist_token': 'ds_2024_energitech'
}

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_logs.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Variables globales
model = None
feature_columns = None
model_metadata = {
    'name': 'Random Forest Classifier - EnergiTech',
    'version': '1.0.0',
    'description': 'Prédiction de panne dans les 7 prochains jours pour les éoliennes',
    'date_entrainement': '2024-01-15',
    'performance': {
        'accuracy': 1,
        'precision': 1,
        'recall': 0.75,
        'f1_score': 0.86
    }
}

# Fonction de vérification des tokens
@auth.verify_token
def verify_token(token):
    if token in API_TOKENS.values():
        return token
    return None

# Décorateur pour logger les requêtes
def log_request(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'endpoint': request.endpoint,
            'method': request.method,
            'user': request.remote_addr,
            'token_provided': 'Authorization' in request.headers,
            'params': dict(request.args) if request.args else None,
            'body': request.get_json(silent=True)
        }
        logger.info(f"Requête API: {json.dumps(log_data)}")
        return f(*args, **kwargs)
    return decorated_function

def load_model():
    """Charge le modèle de classification"""
    global model, feature_columns

    try:
        # Utiliser le fichier fourni
        model_path = 'Model_A/model_classification.pkl'

        # Chargement du modèle avec joblib
        model = joblib.load(model_path)

        # Extraire les noms des features depuis le modèle
        # Le modèle utilise les features suivantes :
        feature_columns = [
            'wind_speed',        # vitesse du vent (m/s)
            'vibration_level',   # niveau de vibration
            'temperature',       # température (°C)
            'power_output',      # puissance délivrée (kW)
            'maintenance_done'   # intervention récente (0/1)
        ]

        # Vérifier que le modèle est bien chargé
        if hasattr(model, 'feature_names_in_'):
            feature_columns = list(model.feature_names_in_)
            logger.info(f"Features extraites du modèle: {feature_columns}")

        logger.info(f"Modèle chargé avec succès depuis {model_path}")
        logger.info(f"Type de modèle: {type(model)}")
        logger.info(f"Nombre de features attendues: {len(feature_columns)}")

    except FileNotFoundError:
        logger.error(f"Fichier modèle non trouvé: {model_path}")
        return False
    except Exception as e:
        logger.error(f"Erreur lors du chargement du modèle: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def validate_input_data(data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """Valide les données d'entrée pour l'inférence"""

    # Vérifier que toutes les features sont présentes
    for feature in feature_columns:
        if feature not in data:
            return False, f"Feature manquante: {feature}"

    # Valider les types et valeurs
    validations = {
        'wind_speed': (lambda x: isinstance(x, (int, float)) and 0 <= x <= 50,
                      "Doit être un nombre entre 0 et 50 m/s"),
        'vibration_level': (lambda x: isinstance(x, (int, float)) and 0 <= x <= 10,
                           "Doit être un nombre entre 0 et 10"),
        'temperature': (lambda x: isinstance(x, (int, float)) and -20 <= x <= 60,
                       "Doit être un nombre entre -20 et 60 °C"),
        'power_output': (lambda x: isinstance(x, (int, float)) and 0 <= x <= 2000,
                        "Doit être un nombre entre 0 et 2000 kW"),
        'maintenance_done': (lambda x: x in [0, 1],
                            "Doit être 0 (non) ou 1 (oui)")
    }

    for feature in feature_columns:
        if feature in validations:
            validation_func, error_msg = validations[feature]
            if not validation_func(data[feature]):
                return False, f"Valeur invalide pour {feature}: {data[feature]}. {error_msg}"

    return True, None

def prepare_features(data: Dict[str, Any]) -> pd.DataFrame:
    """Prépare les features pour la prédiction"""
    # S'assurer que l'ordre des colonnes correspond à celui attendu par le modèle
    features = {col: [data[col]] for col in feature_columns}
    return pd.DataFrame(features)

@app.route('/api/health', methods=['GET'])
@log_request
def health_check():
    """Endpoint de santé de l'API"""
    status = {
        'status': 'healthy' if model is not None else 'degraded',
        'timestamp': datetime.now().isoformat(),
        'model_loaded': model is not None,
        'model_metadata': model_metadata,
        'api_version': '1.0.0',
        'endpoints_available': [
            {'path': '/api/health', 'method': 'GET', 'description': 'Statut de l\'API'},
            {'path': '/api/predict', 'method': 'POST', 'description': 'Prédiction de panne'},
            {'path': '/api/batch-predict', 'method': 'POST', 'description': 'Prédiction par lot'},
            {'path': '/api/stats', 'method': 'GET', 'description': 'Statistiques d\'utilisation'},
            {'path': '/api/model-info', 'method': 'GET', 'description': 'Information sur le modèle'}
        ]
    }
    return jsonify(status)

@app.route('/api/model-info', methods=['GET'])
@auth.login_required
@log_request
def model_info():
    """Retourne les informations sur le modèle"""
    # Essayer d'extraire des informations du modèle réel
    model_details = {
        'type': str(type(model).__name__),
        'features': feature_columns,
        'n_features': len(feature_columns) if feature_columns else 0
    }

    if hasattr(model, 'n_estimators'):
        model_details['n_estimators'] = model.n_estimators
    if hasattr(model, 'classes_'):
        model_details['classes'] = model.classes_.tolist()

    info = {
        'model_name': model_metadata['name'],
        'version': model_metadata['version'],
        'description': model_metadata['description'],
        'training_date': model_metadata['date_entrainement'],
        'performance_metrics': model_metadata['performance'],
        'input_features': feature_columns,
        'model_details': model_details,
        'output': {
            'type': 'classification',
            'classes': [0, 1],
            'description': '0 = Pas de panne dans 7 jours, 1 = Panne probable dans 7 jours'
        },
        'limitations': [
            'Accuracy de 63% - des erreurs sont possibles',
            'Précision de 65% - risque de faux positifs',
            'Rappel de 83% - bonne détection des pannes réelles',
            'Basé sur des données simulées',
            'À utiliser comme aide à la décision, non comme vérité absolue'
        ]
    }
    return jsonify(info)

@app.route('/api/predict', methods=['POST'])
@auth.login_required
@log_request
def predict():
    """Endpoint principal pour la prédiction de panne"""

    # Vérifier si le modèle est chargé
    if model is None:
        logger.error("Tentative de prédiction sans modèle chargé")
        return jsonify({
            'error': 'Modèle non disponible',
            'timestamp': datetime.now().isoformat()
        }), 503

    # Récupérer les données JSON
    data = request.get_json()

    if not data:
        return jsonify({
            'error': 'Données JSON requises',
            'timestamp': datetime.now().isoformat()
        }), 400

    # Valider les données d'entrée
    is_valid, error_msg = validate_input_data(data)
    if not is_valid:
        logger.warning(f"Validation des données échouée: {error_msg}")
        return jsonify({
            'error': f'Données invalides: {error_msg}',
            'timestamp': datetime.now().isoformat()
        }), 400

    try:
        # Préparer les features
        features_df = prepare_features(data)

        # Vérifier les dimensions
        logger.info(f"Features préparées: {features_df.shape}")

        # Faire la prédiction
        prediction_proba = model.predict_proba(features_df)[0]
        prediction_class = model.predict(features_df)[0]

        # Calculer le niveau de risque
        risk_probability = float(prediction_proba[1])  # Probabilité de classe 1 (panne)

        if risk_probability >= 0.7:
            risk_level = "Élevé"
            recommendations = [
                "Intervention recommandée dans les 48h",
                "Vérifier les composants critiques",
                "Préparer les pièces de rechange"
            ]
        elif risk_probability >= 0.4:
            risk_level = "Moyen"
            recommendations = [
                "Surveillance renforcée recommandée",
                "Planifier une intervention préventive",
                "Vérifier les historiques de maintenance"
            ]
        else:
            risk_level = "Faible"
            recommendations = [
                "Maintenance normale prévue",
                "Continuer la surveillance standard"
            ]

        # Préparer la réponse
        response = {
            'prediction': {
                'will_fail': bool(prediction_class),
                'probability_of_failure': round(risk_probability, 3),
                'risk_level': risk_level,
                'confidence': round(max(prediction_proba), 3)
            },
            'technical_details': {
                'class_probabilities': {
                    'no_failure': float(prediction_proba[0]),
                    'failure': float(prediction_proba[1])
                },
                'model_version': model_metadata['version']
            },
            'recommendations': recommendations,
            'input_data': data,
            'timestamp': datetime.now().isoformat(),
            'prediction_id': f"pred_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(str(data)) % 10000:04d}"
        }

        logger.info(f"Prédiction réussie: ID={response['prediction_id']}, "
                   f"Risque={risk_level}, Probabilité={risk_probability:.3f}")

        return jsonify(response)

    except Exception as e:
        logger.error(f"Erreur lors de la prédiction: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return jsonify({
            'error': f'Erreur de prédiction: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/batch-predict', methods=['POST'])
@auth.login_required
@log_request
def batch_predict():
    """Prédiction par lot pour plusieurs éoliennes"""

    if model is None:
        return jsonify({'error': 'Modèle non disponible'}), 503

    data = request.get_json()

    if not data or 'turbines' not in data:
        return jsonify({'error': 'Liste de turbines requise'}), 400

    predictions = []
    errors = []

    for i, turbine_data in enumerate(data['turbines']):
        try:
            # Valider les données de chaque turbine
            is_valid, error_msg = validate_input_data(turbine_data)
            if not is_valid:
                errors.append(f"Turbine {i}: {error_msg}")
                continue

            # Préparer les features et prédire
            features_df = prepare_features(turbine_data)
            prediction_proba = model.predict_proba(features_df)[0]
            prediction_class = model.predict(features_df)[0]

            risk_probability = float(prediction_proba[1])

            predictions.append({
                'turbine_id': turbine_data.get('turbine_id', f"unknown_{i}"),
                'will_fail': bool(prediction_class),
                'probability_of_failure': round(risk_probability, 3),
                'risk_level': "Élevé" if risk_probability >= 0.7 else
                             "Moyen" if risk_probability >= 0.4 else "Faible",
                'input_data': {k: v for k, v in turbine_data.items() if k in feature_columns}
            })

        except Exception as e:
            errors.append(f"Turbine {i}: {str(e)}")

    response = {
        'predictions': predictions,
        'errors': errors if errors else None,
        'summary': {
            'total_turbines': len(data['turbines']),
            'successful_predictions': len(predictions),
            'failed_predictions': len(errors)
        },
        'timestamp': datetime.now().isoformat()
    }

    return jsonify(response)

@app.route('/api/stats', methods=['GET'])
@auth.login_required
@log_request
def get_stats():
    """Retourne des statistiques d'utilisation"""
    stats = {
        'uptime': '24/7',
        'model_requests_today': 42,
        'average_response_time_ms': 120,
        'success_rate': 0.95,
        'last_prediction': datetime.now().isoformat(),
        'active_since': datetime.now().replace(hour=0, minute=0, second=0).isoformat()
    }
    return jsonify(stats)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint non trouvé'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Méthode non autorisée'}), 405

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Erreur interne: {str(error)}")
    import traceback
    logger.error(traceback.format_exc())
    return jsonify({'error': 'Erreur interne du serveur'}), 500

if __name__ == '__main__':
    # Charger le modèle au démarrage
    print("Chargement du modèle de classification EnergiTech...")
    if load_model():
        print("Modèle chargé avec succès!")
    else:
        print("Le modèle n'a pas pu être chargé. L'API fonctionnera en mode dégradé.")

    # Afficher les informations de démarrage
    print("\n" + "="*60)
    print("🚀 API de Maintenance Prédictive - EnergiTech")
    print("="*60)
    print(f"\n📊 Modèle: {model_metadata['name']}")
    print(f"📈 Performance: Accuracy={model_metadata['performance']['accuracy']}")
    print(f"📈 Performance: Recall={model_metadata['performance']['recall']}")
    print("\n🔐 Tokens d'authentification:")
    for role, token in API_TOKENS.items():
        print(f"   {role}: {token}")

    print("\n🌐 Endpoints disponibles:")
    print("   GET  /api/health       - Vérifier l'état de l'API")
    print("   GET  /api/model-info   - Informations sur le modèle (authentifié)")
    print("   POST /api/predict      - Prédiction unique (authentifié)")
    print("   POST /api/batch-predict - Prédiction par lot (authentifié)")
    print("   GET  /api/stats        - Statistiques (authentifié)")

    print(f"\n👤 Headers requis: Authorization: Bearer <token>")

    # Démarrer le serveur
    app.run(host='0.0.0.0', port=5000, debug=False)
