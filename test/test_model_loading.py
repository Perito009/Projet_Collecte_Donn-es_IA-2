import ApiPredictDays as mi
import joblib


def test_model_load_success(monkeypatch):
    """
    Vérifie que le modèle IA se charge correctement (joblib mocké)
    """
    class Dummy:
        feature_names_in_ = ['wind_speed', 'vibration_level', 'temperature', 'power_output', 'maintenance_done']

    # Mock joblib.load pour retourner un modèle factice
    monkeypatch.setattr(joblib, 'load', lambda path: Dummy())

    result = mi.load_model()

    assert result is not False
    assert mi.model is not None
    assert mi.feature_columns is not None
    assert len(mi.feature_columns) > 0
