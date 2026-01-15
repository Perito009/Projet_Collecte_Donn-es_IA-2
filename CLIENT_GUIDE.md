# Guide d'utilisation - Interfaces Client

Ce document explique comment utiliser les différentes interfaces client pour interagir avec l'API de maintenance prédictive EnergiTech.

## Table des matières

1. [Interface Web Streamlit](#interface-web-streamlit)
2. [Client CLI (Ligne de commande)](#client-cli-ligne-de-commande)
3. [Exemples d'utilisation](#exemples-dutilisation)

---

## Interface Web Streamlit

### Démarrage de l'interface

L'interface Streamlit offre une expérience visuelle complète pour interagir avec l'API de prédiction.

#### Prérequis
- Python 3.8+
- API Flask en cours d'exécution sur `http://localhost:5000`

#### Lancement

```bash
# Démarrer l'API (dans un terminal)
python ApiPredictDays.py

# Démarrer l'interface Streamlit (dans un autre terminal)
cd app
streamlit run main.py
```

L'application sera accessible à l'adresse: `http://localhost:8501`

### Fonctionnalités disponibles

#### 1. Page d'accueil et authentification
- Connexion avec identifiants:
  - **Technicien**: `technicien` / `tech123`
  - **Manager**: `manager` / `manager123`

#### 2. 📝 Logs
- Consultation des logs système
- Suivi des activités

#### 3. 📈 Mesures capteurs
- Visualisation en temps réel des données capteurs
- Surveillance des paramètres des éoliennes

#### 4. 📊 Historique & risques
- Analyse de risque unique
- Visualisation de l'évolution du risque sur 7 jours
- Graphiques interactifs
- Recommandations basées sur les prédictions

#### 5. 🔮 Prédictions 7 jours (NOUVEAU)

Cette nouvelle page permet de générer des prédictions pour les 7 prochains jours.

**Fonctionnalités:**

- **Configuration des paramètres de base:**
  - Température de base (°C)
  - Niveau de vibration
  - Vitesse du vent (m/s)
  - Puissance délivrée (kW)
  - État de maintenance

- **Options de variation:**
  - Variation de température (± °C)
  - Variation de vibration (±)
  - Les paramètres varient automatiquement chaque jour pour simuler des conditions réelles

- **Visualisations:**
  - Graphique d'évolution du risque sur 7 jours
  - Statistiques globales (probabilité moyenne, max, jours à risque)
  - Alertes automatiques pour les risques élevés
  - Recommandations personnalisées

- **Export:**
  - Téléchargement des résultats en format CSV
  - Tableau détaillé des prédictions

**Capture d'écran:**

![Prédictions 7 jours](docs/batch_predictions_screenshot.png)

---

## Client CLI (Ligne de commande)

Le client CLI (`cli_client.py`) est un outil en ligne de commande pour les utilisateurs techniques qui préfèrent travailler dans le terminal.

### Installation

Aucune installation supplémentaire n'est nécessaire si vous avez déjà installé les dépendances du projet:

```bash
pip install -r requirements.txt
```

### Commandes disponibles

#### 1. Vérifier l'état de l'API

```bash
python cli_client.py health
```

Affiche:
- Statut de l'API (healthy/degraded)
- État du modèle (chargé/non chargé)
- Version de l'API et du modèle
- Liste des endpoints disponibles

#### 2. Prédiction unique

```bash
python cli_client.py predict \
  --wind-speed 12.5 \
  --vibration 4.2 \
  --temperature 28.0 \
  --power 850 \
  --maintenance 0
```

Affiche:
- Niveau de risque (Faible/Moyen/Élevé)
- Probabilité de panne
- Prédiction de panne (OUI/NON)
- Confiance du modèle
- Recommandations

#### 3. Prédictions sur 7 jours

```bash
python cli_client.py predict-7days \
  --turbine-id WIND-001 \
  --wind-speed 10 \
  --vibration 3 \
  --temperature 25 \
  --power 700 \
  --maintenance 0
```

Affiche:
- Prédictions pour chaque jour
- Statistiques globales
- Nombre de turbines à risque élevé/moyen/faible
- Nombre de pannes prédites
- Détails pour chaque jour

#### 4. Informations sur le modèle

```bash
python cli_client.py model-info
```

Affiche:
- Nom et version du modèle
- Date d'entraînement
- Métriques de performance
- Features d'entrée
- Limitations

### Options avancées

#### Utiliser un token différent

Par défaut, le CLI utilise le token technicien. Pour utiliser un autre token:

```bash
python cli_client.py predict \
  --token manager_2024_energitech \
  --wind-speed 12.5 \
  --vibration 4.2 \
  --temperature 28.0 \
  --power 850 \
  --maintenance 0
```

Tokens disponibles:
- `tech_2024_energitech` (technicien) - par défaut
- `manager_2024_energitech` (manager)
- `ds_2024_energitech` (data scientist)

#### Aide et documentation

```bash
python cli_client.py --help
```

---

## Exemples d'utilisation

### Scénario 1: Surveillance quotidienne (CLI)

```bash
# 1. Vérifier que l'API fonctionne
python cli_client.py health

# 2. Faire une analyse rapide
python cli_client.py predict \
  --wind-speed 15.0 \
  --vibration 5.0 \
  --temperature 30.0 \
  --power 1200 \
  --maintenance 0

# 3. Si le risque est élevé, obtenir plus d'infos
python cli_client.py model-info
```

### Scénario 2: Planification hebdomadaire (Streamlit)

1. Ouvrir l'interface Streamlit
2. Se connecter en tant que **manager**
3. Aller sur la page **🔮 Prédictions 7 jours**
4. Entrer les paramètres de l'éolienne à surveiller
5. Ajuster les variations pour des prédictions réalistes
6. Générer les prédictions
7. Analyser les graphiques et alertes
8. Exporter les résultats en CSV pour partage
9. Planifier les interventions selon les recommandations

### Scénario 3: Analyse de flotte (CLI)

```bash
# Analyser plusieurs turbines sur 7 jours
for turbine in WIND-001 WIND-002 WIND-003; do
  echo "Analyse de $turbine"
  python cli_client.py predict-7days \
    --turbine-id $turbine \
    --wind-speed 12 \
    --vibration 3.5 \
    --temperature 26 \
    --power 800 \
    --maintenance 0
  echo "---"
done
```

### Scénario 4: Intégration dans un script de monitoring

```python
#!/usr/bin/env python3
import subprocess
import json

def check_turbine_health(turbine_data):
    """
    Vérifie la santé d'une turbine via le CLI
    """
    cmd = [
        'python', 'cli_client.py', 'predict',
        '--wind-speed', str(turbine_data['wind_speed']),
        '--vibration', str(turbine_data['vibration']),
        '--temperature', str(turbine_data['temperature']),
        '--power', str(turbine_data['power']),
        '--maintenance', str(turbine_data['maintenance'])
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

# Utilisation
turbine = {
    'wind_speed': 15.0,
    'vibration': 4.5,
    'temperature': 28.0,
    'power': 1100,
    'maintenance': 0
}

if check_turbine_health(turbine):
    print("Turbine OK")
else:
    print("Turbine à risque - intervention requise")
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Utilisateurs                          │
│                                                          │
│  ┌──────────────┐           ┌──────────────────┐       │
│  │   Managers   │           │   Techniciens    │       │
│  │   Engineers  │           │   Operators      │       │
│  └──────┬───────┘           └────────┬─────────┘       │
│         │                            │                  │
└─────────┼────────────────────────────┼──────────────────┘
          │                            │
          ▼                            ▼
   ┌─────────────┐            ┌──────────────┐
   │  Streamlit  │            │  CLI Client  │
   │     Web     │            │   Terminal   │
   │  Interface  │            │    Script    │
   └──────┬──────┘            └──────┬───────┘
          │                          │
          └────────────┬─────────────┘
                       │
                       ▼
              ┌────────────────┐
              │   Flask API    │
              │  localhost:5000│
              └────────┬───────┘
                       │
                       ▼
              ┌────────────────┐
              │  ML Model      │
              │  Random Forest │
              └────────────────┘
```

---

## Dépannage

### L'API ne répond pas

```bash
# Vérifier que l'API est démarrée
python cli_client.py health

# Si erreur, redémarrer l'API
python ApiPredictDays.py
```

### Erreur d'authentification

- Vérifier que vous utilisez le bon token
- Les tokens disponibles sont dans `ApiPredictDays.py`

### Streamlit ne démarre pas

```bash
# Vérifier que vous êtes dans le bon répertoire
cd app
streamlit run main.py

# Si erreur de module manquant
pip install -r ../requirements.txt
```

### Prédictions incorrectes

- Vérifier que les valeurs des paramètres sont dans les plages valides:
  - Vitesse du vent: 0-50 m/s
  - Vibration: 0-10
  - Température: -20 à 60 °C
  - Puissance: 0-2000 kW
  - Maintenance: 0 ou 1

---

## Support et Contact

Pour toute question ou problème:

1. Consulter la documentation de l'API: `swagger.yaml`
2. Vérifier les logs: `api_logs.log`
3. Utiliser `python cli_client.py --help` pour l'aide CLI

---

## Prochaines évolutions

- [ ] Export des prédictions en PDF
- [ ] Notifications automatiques par email
- [ ] Intégration avec systèmes de monitoring existants
- [ ] API REST pour automatisation complète
- [ ] Dashboard temps réel avec WebSocket
- [ ] Historique des prédictions en base de données
