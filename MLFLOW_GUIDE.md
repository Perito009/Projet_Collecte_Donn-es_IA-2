# 📊 Guide MLflow pour le Notebook ETL_MSPR2

## 🎯 Vue d'ensemble

Le notebook **ETL_MSPR2.ipynb** a été adapté pour intégrer complètement **MLflow**, un outil puissant de suivi et de gestion des expériences de Machine Learning.

## ✨ Améliorations apportées

### 1. **Configuration MLflow**
- ✅ Répertoire de suivi configuré : `/content/mlruns`
- ✅ Deux expériences distinctes :
  - `Turbine_Failure_Prediction_Classification` (Modèle A)
  - `Turbine_Time_to_Failure_Prediction_Regression` (Modèle B)

### 2. **Modèle A - Classification (Prédiction de pannes)**
**Cellule adaptée** : Cellule avec `model_A`

**Paramètres enregistrés :**
- `features` : Features utilisées
- `target` : Variable cible (`failure_within_7d`)
- `test_size`, `random_state`, `stratify`
- `model_type`, `model_source`

**Métriques enregistrées :**
- 📈 `accuracy` - Précision globale
- 📈 `precision` - Précision (vrais positifs / positifs prédits)
- 📈 `recall` - Rappel (vrais positifs / vrais positifs réels)
- 📈 `f1_score` - Harmonie entre précision et rappel
- 📈 `roc_auc` - Score AUC-ROC

**Artifacts enregistrés :**
- 📊 `confusion_matrix_model_a.html` - Matrice de confusion interactive
- 📊 `roc_curve_model_a.html` - Courbe ROC interactive
- 🤖 `classification_model` - Modèle sérialisé

### 3. **Modèle B - Régression (Temps jusqu'à la panne)**
**Cellule adaptée** : Cellule avec `model_B`

**Paramètres enregistrés :**
- `features` : Features utilisées
- `target` : Variable cible (`time_to_failure_days`)
- `test_size_reg`, `random_state_reg`
- `model_type`, `model_source`

**Métriques enregistrées :**
- 📈 `mae` - Erreur absolue moyenne
- 📈 `mse` - Erreur quadratique moyenne
- 📈 `rmse` - Racine de l'erreur quadratique moyenne
- 📈 `r2_score` - Coefficient de détermination

**Artifacts enregistrés :**
- 📊 `regression_predictions_plot.html` - Scatter plot des prédictions
- 📊 `error_distribution.html` - Distribution des erreurs
- 🤖 `regression_model` - Modèle sérialisé

### 4. **Lancement du serveur MLflow UI**
**Cellule dédiée** : Cellule de lancement du serveur

La cellule lance automatiquement le serveur MLflow sur le port 5000 avec :
- 🌐 Interface web interactive
- 📊 Visualisation des expériences
- 📈 Comparaison des runs
- 🎯 Affichage des paramètres et métriques

### 5. **Dashboard Récapitulatif**
**Cellule finale** : Résumé des exécutions MLflow

Affiche un résumé complet dans la console :
- Liste de toutes les expériences
- Détails de chaque run
- Paramètres clés
- Métriques principales

## 🚀 Comment utiliser

### Étape 1 : Exécuter le notebook complet

```python
# Le notebook exécutera dans l'ordre :
1. Chargement des données (Google Drive)
2. Nettoyage et préparation des données
3. Analyse exploratoire (EDA)
4. Entraînement du Modèle A (Classification) ✓ MLflow
5. Entraînement du Modèle B (Régression) ✓ MLflow
6. Lancement du serveur MLflow UI
7. Affichage du dashboard récapitulatif
```

### Étape 2 : Accéder à MLflow UI

#### En environnement local :
```bash
mlflow ui --backend-store-uri file:///content/mlruns --host 0.0.0.0 --port 5000
```

Puis ouvrir dans le navigateur : **http://localhost:5000**

#### En Colab :
La cellule de lancement gère tout automatiquement.

### Étape 3 : Explorer les résultats

Dans MLflow UI, vous pouvez :

#### 🔍 Comparer les modèles
- Sélectionner plusieurs runs
- Comparer côte à côte les métriques
- Visualiser les différences de performance

#### 📊 Consulter les artifacts
- Télécharger les graphiques HTML
- Consulter les modèles sérialisés
- Analyser les visualisations Plotly

#### 📈 Analyser les paramètres
- Voir quels paramètres affectent les performances
- Tracer des graphiques de paramètres vs métriques
- Identifier les meilleurs hyperparamètres

## 📁 Structure MLflow

```
mlruns/
├── 0/                              # Expérience par défaut
├── 1/                              # Turbine_Failure_Prediction_Classification
│   └── <run_id>/
│       ├── params/                 # Paramètres du run
│       ├── metrics/                # Métriques enregistrées
│       ├── artifacts/              # Graphiques et modèles
│       ├── meta.yaml               # Métadonnées du run
│       └── tags/                   # Tags personnalisés
└── 2/                              # Turbine_Time_to_Failure_Prediction_Regression
    └── <run_id>/
        ├── params/
        ├── metrics/
        ├── artifacts/
        └── ...
```

## 🎯 Métriques clés expliquées

### Classification (Modèle A)

| Métrique | Formule | Interprétation |
|----------|---------|-----------------|
| **Accuracy** | (TP+TN)/(TP+TN+FP+FN) | % de prédictions correctes |
| **Precision** | TP/(TP+FP) | % de pannes prédites qui sont réelles |
| **Recall** | TP/(TP+FN) | % de vraies pannes détectées |
| **F1-Score** | 2×(P×R)/(P+R) | Moyenne harmonique P et R |
| **ROC-AUC** | 0-1 | Capacité de discrimination (0.5=aléatoire, 1=parfait) |

### Régression (Modèle B)

| Métrique | Formule | Interprétation |
|----------|---------|-----------------|
| **MAE** | Σ\|y-ŷ\|/n | Erreur moyenne en jours |
| **RMSE** | √(Σ(y-ŷ)²/n) | Pénalise les grandes erreurs |
| **R²** | 1 - (SS_res/SS_tot) | % de variance expliquée (0-1) |

## 💡 Conseils d'utilisation

### ✅ Bonnes pratiques

1. **Nommer vos runs** : Les noms rendent les comparaisons plus faciles
2. **Utiliser des tags** : Vous pouvez ajouter `mlflow.set_tag("production", "true")`
3. **Documenter les changements** : Notez les modifications apportées aux features
4. **Comparer régulièrement** : Suivez l'évolution des performances

### 🔄 Améliorer les modèles

Pour relancer avec de nouveaux paramètres :

```python
# Modifiez les hyperparamètres dans la cellule du modèle
max_depth = 15  # au lieu de 10

# Le notebook créera un nouveau run MLflow automatiquement
```

## 🔗 Intégration avancée

### Intégration avec une base de données

Pour une utilisation en production, stockez MLflow sur un serveur distant :

```python
mlflow.set_tracking_uri("postgresql://user:password@localhost/mlflow")
```

### Déploiement de modèles

Sauvegarder un modèle en registre :

```python
mlflow.register_model("runs:/<run_id>/model_name", "Model_A_Production")
```

## 📞 Dépannage

### Problème : Port 5000 déjà utilisé

**Solution :** Changer le port dans la cellule de lancement
```python
subprocess.Popen(["mlflow", "ui", "--port", "5001"])
```

### Problème : Données non persistantes

**Solution :** Utiliser une URI de backend persistante
```python
mlflow.set_tracking_uri("postgresql://...")  # Base de données
```

### Problème : Artifacts non visibles

**Solution :** Vérifier que le chemin des artifacts existe
```python
import os
os.makedirs("/content/mlruns", exist_ok=True)
```

## 📚 Ressources supplémentaires

- 📖 [Documentation officielle MLflow](https://mlflow.org/docs)
- 🎓 [Tutoriels MLflow](https://mlflow.org/docs/latest/tutorials-and-examples)
- 🔗 [Comparaison des runs](https://mlflow.org/docs/latest/tracking)

## ✅ Checklist de vérification

Après chaque exécution du notebook :

- [ ] ✅ Deux expériences créées dans MLflow
- [ ] ✅ Paramètres du Modèle A enregistrés
- [ ] ✅ Métriques du Modèle A enregistrées (accuracy, precision, recall, f1, roc_auc)
- [ ] ✅ Artifacts du Modèle A disponibles (confusion_matrix, roc_curve)
- [ ] ✅ Paramètres du Modèle B enregistrés
- [ ] ✅ Métriques du Modèle B enregistrées (mae, rmse, r2)
- [ ] ✅ Artifacts du Modèle B disponibles (scatter plot, error distribution)
- [ ] ✅ Serveur MLflow lancé avec succès
- [ ] ✅ Dashboard récapitulatif affiché
- [ ] ✅ Interface MLflow accessible sur http://localhost:5000

---

**Créé le :** Février 2026  
**Version :** 1.0  
**Statut :** ✅ Production-ready
