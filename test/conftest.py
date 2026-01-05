import sys
import os
import pytest

# Assurer que le répertoire racine du projet est dans le PYTHONPATH pour importer le module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import ApiPredictDays as mi

@pytest.fixture
def client():
    """Fixture fournissant un test client Flask configuré pour les tests."""
    mi.app.config['TESTING'] = True
    with mi.app.test_client() as client:
        yield client
