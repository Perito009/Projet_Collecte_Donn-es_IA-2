import ApiPredictDays as mi
import pandas as pd

mi.load_model()

def test_prepare_features_shape_and_columns():
    data = {
        "wind_speed": 10,
        "vibration_level": 2,
        "temperature": 20,
        "power_output": 900,
        "maintenance_done": 1
    }

    df = mi.prepare_features(data)

    assert isinstance(df, pd.DataFrame)
    assert df.shape == (1, len(mi.feature_columns))
    assert list(df.columns) == mi.feature_columns


def test_model_prediction_output():
    data = {
        "wind_speed": 14.2,
        "vibration_level": 4.1,
        "temperature": 30,
        "power_output": 1100,
        "maintenance_done": 0
    }

    features_df = mi.prepare_features(data)

    # Prédiction
    prediction = mi.model.predict(features_df)
    prediction_proba = mi.model.predict_proba(features_df)

    # Assertions
    assert prediction.shape == (1,)
    assert prediction[0] in [0, 1]

    assert prediction_proba.shape == (1, 2)
    assert 0.0 <= prediction_proba[0][0] <= 1.0
    assert 0.0 <= prediction_proba[0][1] <= 1.0

    # Les probabilités doivent sommer à 1
    assert round(sum(prediction_proba[0]), 5) == 1.0
def test_model_prediction_consistency():
    data = {
        "wind_speed": 8.5,
        "vibration_level": 1.5,
        "temperature": 15,
        "power_output": 750,
        "maintenance_done": 1
    }

    features_df = mi.prepare_features(data)

    # Prédictions multiples
    prediction1 = mi.model.predict(features_df)
    prediction2 = mi.model.predict(features_df)

    # Vérifier la cohérence des prédictions
    assert prediction1[0] == prediction2[0]
