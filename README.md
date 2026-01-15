# Projet_Collecte_Donn-es_IA-2

## 🚀 Système de Maintenance Prédictive pour Éoliennes - EnergiTech

Ce projet fournit une solution complète de maintenance prédictive pour les éoliennes, incluant :
- Une API REST Flask pour les prédictions
- Une interface web Streamlit pour la visualisation
- Un client CLI pour l'automatisation
- Un modèle de Machine Learning (Random Forest) pour détecter les pannes

## 📋 Table des Matières

1. [Installation](#installation)
2. [Démarrage Rapide](#démarrage-rapide)
3. [Interfaces Disponibles](#interfaces-disponibles)
4. [Documentation](#documentation)
5. [Architecture](#architecture)

## 🔧 Installation

```bash
# Cloner le repository
git clone https://github.com/Perito009/Projet_Collecte_Donn-es_IA-2.git
cd Projet_Collecte_Donn-es_IA-2

# Installer les dépendances
pip install -r requirements.txt
```

## 🚀 Démarrage Rapide
Soit vous pouvez demarer le back et le front avec le .sh ou alors suivre les steps ci-dessous
```bash
python ./main_project.sh
``` 

### 1. Démarrer l'API

```bash
python ApiPredictDays.py
```

L'API sera disponible sur `http://localhost:5000`

### 2. Utiliser le CLI (Terminal)

```bash
# Vérifier l'état de l'API
python cli_client.py health

# Faire une prédiction
python cli_client.py predict --wind-speed 12.5 --vibration 4.2 --temperature 28.0 --power 850 --maintenance 0

# Prédictions sur 7 jours
python cli_client.py predict-7days --turbine-id WIND-001 --wind-speed 10 --vibration 3 --temperature 25 --power 700 --maintenance 0
```

### 3. Utiliser l'Interface Web Streamlit

```bash
cd app
streamlit run main.py
```

L'interface sera disponible sur `http://localhost:8501`

**Identifiants:**
- Manager: `manager` / `manager123`
- Technicien: `technicien` / `tech123`

## 🎯 Interfaces Disponibles

### 1. 🌐 Interface Web Streamlit

Interface graphique complète avec :
- **📝 Logs** - Consultation des journaux système
- **📈 Mesures capteurs** - Visualisation des données en temps réel
- **📊 Historique & risques** - Analyse et graphiques de risque
- **🔮 Prédictions 7 jours** - Prédictions par lot sur 7 jours *(NOUVEAU)*

#### Page Prédictions 7 jours
- Configuration des paramètres de base
- Visualisation interactive des risques
- Statistiques détaillées
- Export CSV
- Recommandations automatiques

### 2. 💻 Client CLI

Outil en ligne de commande pour :
- Vérification de l'état de l'API
- Prédictions uniques
- Prédictions sur 7 jours
- Informations sur le modèle
- Intégration dans des scripts d'automatisation

**Commandes disponibles:**
```bash
cli_client.py health              # État de l'API
cli_client.py predict [options]   # Prédiction unique
cli_client.py predict-7days [options]  # 7 jours
cli_client.py model-info          # Info modèle
```

### 3. 🔄 Script d'Automatisation

Exemple d'intégration dans un système de surveillance :
```bash
python example_automation.py
```

Ce script montre comment :
- Surveiller plusieurs turbines automatiquement
- Générer des rapports de synthèse
- Déclencher des alertes selon les niveaux de risque

## 📚 Documentation

- **[CLIENT_GUIDE.md](CLIENT_GUIDE.md)** - Guide complet d'utilisation des interfaces
- **[swagger.yaml](swagger.yaml)** - Documentation de l'API REST
- **api_logs.log** - Logs de l'API

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         Utilisateurs                     │
│  Managers | Techniciens | Scripts       │
└──────────┬──────────────┬───────────────┘
           │              │
    ┌──────▼──────┐  ┌───▼─────┐
    │  Streamlit  │  │   CLI   │
    │     Web     │  │  Client │
    └──────┬──────┘  └───┬─────┘
           │             │
           └──────┬──────┘
                  │
         ┌────────▼────────┐
         │   Flask API     │
         │  Port 5000      │
         └────────┬────────┘
                  │
         ┌────────▼────────┐
         │  ML Model       │
         │ Random Forest   │
         └─────────────────┘
```

## 🔑 Endpoints API

- `GET /api/health` - État de l'API (public)
- `POST /api/predict` - Prédiction unique (authentifié)
- `POST /api/batch-predict` - Prédiction par lot (authentifié)
- `GET /api/model-info` - Informations du modèle (authentifié)
- `GET /api/stats` - Statistiques d'utilisation (authentifié)

## 🔐 Authentification

Tokens disponibles :
- `tech_2024_energitech` - Technicien
- `manager_2024_energitech` - Manager
- `ds_2024_energitech` - Data Scientist

Headers requis : `Authorization: Bearer <token>`

## 📊 Modèle ML

- **Type** : Random Forest Classifier
- **Prédiction** : Panne dans les 7 prochains jours
- **Features** : wind_speed, vibration_level, temperature, power_output, maintenance_done
- **Performance** : Accuracy 63%, Recall 83%

## 🛠️ Développement

```bash
# Tests
pytest test/

# Structure du projet
├── ApiPredictDays.py          # API Flask
├── cli_client.py              # Client CLI
├── example_automation.py      # Exemple d'automatisation
├── app/                       # Interface Streamlit
│   ├── main.py
│   ├── batch_predictions.py   # Page prédictions 7 jours
│   ├── historiques.py
│   └── ...
├── Model_A/                   # Modèle ML
│   └── model_classification.pkl
└── test/                      # Tests
```

## 📝 License

MIT License

## 👥 Contributeurs

- EnergiTech Team

## 📞 Support

Pour toute question, consulter le [CLIENT_GUIDE.md](CLIENT_GUIDE.md) ou les logs dans `api_logs.log`.
