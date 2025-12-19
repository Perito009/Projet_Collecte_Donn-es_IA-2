import ApiPredictDays as mi

def test_model_load_success():
    """
    Vérifie que le modèle IA se charge correctement
    """
    result = mi.load_model()

    assert result is not False
    assert mi.model is not None
    assert mi.feature_columns is not None
    assert len(mi.feature_columns) > 0
