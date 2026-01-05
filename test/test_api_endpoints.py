import ApiPredictDays as mi
import pytest
from unittest.mock import Mock

# Headers d'authentification utilisés dans les tests
AUTH_HEADER = {'Authorization': 'Bearer manager_2024_energitech'}
TECH_HEADER = {'Authorization': 'Bearer tech_2024_energitech'}


class DummyModel:
    """Petit modèle factice pour contrôler les sorties de prédiction."""
    def __init__(self):
        self.feature_names_in_ = [
            'wind_speed', 'vibration_level', 'temperature', 'power_output', 'maintenance_done'
        ]
        self.n_estimators = 10
        import numpy as _np
        self.classes_ = _np.array([0, 1])

    def predict_proba(self, X):
        # Si wind_speed > 12 => forte probabilité de panne
        ws = X.iloc[0]['wind_speed']
        if ws > 12:
            return [[0.1, 0.9]]
        return [[0.8, 0.2]]

    def predict(self, X):
        return [int(self.predict_proba(X)[0][1] >= 0.5)]


def setup_dummy_model():
    dummy = DummyModel()
    mi.model = dummy
    mi.feature_columns = list(dummy.feature_names_in_)


def teardown_dummy_model():
    mi.model = None
    mi.feature_columns = None


def test_health_check_degraded(client):
    # Pas de modèle chargé => état dégradé
    mi.model = None
    res = client.get('/api/health')
    assert res.status_code == 200
    data = res.get_json()
    assert data['status'] == 'degraded'
    assert data['model_loaded'] is False


def test_model_info_requires_auth(client):
    res = client.get('/api/model-info')
    assert res.status_code == 401


def test_model_info_with_token(client):
    setup_dummy_model()
    res = client.get('/api/model-info', headers=AUTH_HEADER)
    assert res.status_code == 200
    data = res.get_json()
    assert data['model_name'] == mi.model_metadata['name']
    assert 'input_features' in data
    teardown_dummy_model()


def test_predict_success(client):
    setup_dummy_model()
    payload = {
        "wind_speed": 15,
        "vibration_level": 2,
        "temperature": 20,
        "power_output": 900,
        "maintenance_done": 1
    }

    res = client.post('/api/predict', json=payload, headers=TECH_HEADER)
    assert res.status_code == 200
    data = res.get_json()
    assert 'prediction' in data
    assert data['prediction']['probability_of_failure'] == 0.9
    assert data['prediction']['risk_level'] == "Élevé"
    teardown_dummy_model()


def test_predict_invalid_json(client):
    setup_dummy_model()
    # Corps absent / JSON invalide
    # Envoyer explicitement 'null' pour que request.get_json() retourne None sans lever d'exception
    res = client.post('/api/predict', data='null', headers=TECH_HEADER, content_type='application/json')
    assert res.status_code == 400
    data = res.get_json()
    assert 'Données JSON requises' in data['error']
    teardown_dummy_model()


def test_predict_invalid_input(client):
    setup_dummy_model()
    payload = {
        "wind_speed": 15,
        "vibration_level": 2,
        "temperature": 20,
        "power_output": 900
        # "maintenance_done" manquant
    }

    res = client.post('/api/predict', json=payload, headers=TECH_HEADER)
    assert res.status_code == 400
    data = res.get_json()
    assert 'Feature manquante' in data['error']
    teardown_dummy_model()


def test_predict_model_not_loaded(client):
    mi.model = None
    payload = {
        "wind_speed": 10,
        "vibration_level": 1,
        "temperature": 10,
        "power_output": 500,
        "maintenance_done": 0
    }

    res = client.post('/api/predict', json=payload, headers=TECH_HEADER)
    assert res.status_code == 503
    data = res.get_json()
    assert 'Modèle non disponible' in data['error']


def test_batch_predict_success(client):
    setup_dummy_model()
    payload = {
        "turbines": [
            {
                "turbine_id": "t1",
                "wind_speed": 14,
                "vibration_level": 2,
                "temperature": 20,
                "power_output": 900,
                "maintenance_done": 1
            },
            {
                "turbine_id": "t2",
                "wind_speed": 8,
                "vibration_level": 1,
                "temperature": 15,
                "power_output": 700,
                "maintenance_done": 0
            }
        ]
    }

    res = client.post('/api/batch-predict', json=payload, headers=TECH_HEADER)
    assert res.status_code == 200
    data = res.get_json()
    assert 'predictions' in data
    assert len(data['predictions']) == 2
    assert data['summary']['successful_predictions'] == 2
    teardown_dummy_model()


def test_batch_predict_bad_request(client):
    setup_dummy_model()
    res = client.post('/api/batch-predict', json={}, headers=TECH_HEADER)
    assert res.status_code == 400
    data = res.get_json()
    assert 'Liste de turbines requise' in data['error']
    teardown_dummy_model()


def test_stats_requires_auth(client):
    res = client.get('/api/stats')
    assert res.status_code == 401


def test_stats_with_auth(client):
    setup_dummy_model()
    res = client.get('/api/stats', headers=AUTH_HEADER)
    assert res.status_code == 200
    data = res.get_json()
    assert 'uptime' in data
    teardown_dummy_model()
