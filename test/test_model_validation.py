import ApiPredictDays as mi

# Charger le modèle une fois pour tous les tests
mi.load_model()

def test_validate_input_data_valid():
    valid_data = {
        "wind_speed": 12.5,
        "vibration_level": 3.2,
        "temperature": 25,
        "power_output": 850,
        "maintenance_done": 0
    }

    is_valid, error = mi.validate_input_data(valid_data)

    assert is_valid is True
    assert error is None


def test_validate_input_data_missing_feature():
    invalid_data = {
        "wind_speed": 12.5,
        "vibration_level": 3.2,
        "temperature": 25,
        "power_output": 850
        # maintenance_done manquant
    }

    is_valid, error = mi.validate_input_data(invalid_data)

    assert is_valid is False
    assert "Feature manquante" in error


def test_validate_input_data_invalid_value():
    invalid_data = {
        "wind_speed": 120,  # invalide
        "vibration_level": 3.2,
        "temperature": 25,
        "power_output": 850,
        "maintenance_done": 0
    }

    is_valid, error = mi.validate_input_data(invalid_data)

    assert is_valid is False
    assert "Valeur invalide" in error
