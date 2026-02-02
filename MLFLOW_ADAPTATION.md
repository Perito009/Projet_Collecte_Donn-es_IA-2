# 📊 Adaptation MLflow du Notebook ETL_MSPR2

## 🎯 Résumé des modifications

Votre notebook **ETL_MSPR2.ipynb** a été complètement adapté pour intégrer **MLflow**, l'outil de suivi des expériences de Machine Learning. Toutes les modifications conservent votre code original tout en ajoutant des fonctionnalités professionnelles de suivi et de documentation.

## ✨ Changements effectués

### 1. **Cellule d'installation MLflow** 
**Avant :**
```python
!pip install MLflow
```

**Après :**
```python
!pip install mlflow -q
print("MLflow installé avec succès")
```
- ✅ Installation silencieuse (`-q`)
- ✅ Confirmation du succès

### 2. **Modèle A - Classification (Adaptée)**

**Améliorations :**
- ✅ Configuration centralisée de MLflow
- ✅ Création automatique du répertoire `/content/mlruns`
- ✅ Enregistrement complet de l'expérience
- ✅ Suivi de tous les paramètres (features, target, hyperparamètres)
- ✅ Enregistrement des 5 métriques essentielles :
  - `accuracy`
  - `precision`
  - `recall`
  - `f1_score`
  - `roc_auc` *(nouvelle)*
  
- ✅ Artifacts enregistrés :
  - Matrice de confusion (HTML interactif)
  - Courbe ROC (HTML interactif)
  - Modèle sérialisé

**Code original conservé :**
- Chargement du modèle existant
- Entraînement si nécessaire
- Visualisations Plotly
- Affichage des métriques

### 3. **Modèle B - Régression (Adaptée)**

**Améliorations :**
- ✅ Configuration MLflow dédiée
- ✅ Suivi des paramètres de régression
- ✅ Enregistrement des 4 métriques :
  - `mae` (erreur absolue moyenne)
  - `mse` (erreur quadratique moyenne)
  - `rmse` (racine de MSE)
  - `r2_score` (coefficient de détermination)
  
- ✅ Artifacts enregistrés :
  - Scatter plot (prédictions vs réalité)
  - Distribution des erreurs
  - Modèle sérialisé

- ✅ Nouvelles visualisations :
  - Distribution des erreurs de prédiction
  - Meilleure présentation du scatter plot

### 4. **Serveur MLflow UI (Nouvelle cellule)**

**Fonctionnalité :**
```python
# Lance automatiquement le serveur MLflow
mlflow ui --backend-store-uri file:///content/mlruns
```

**Avantages :**
- 🌐 Interface web interactive
- 📊 Visualisation complète des expériences
- 🔄 Comparaison facile entre runs
- 📥 Téléchargement des artifacts
- 📈 Graphiques et tableaux interactifs

**Accès :**
- Local : `http://localhost:5000`
- À distance : `http://<ip-serveur>:5000`

### 5. **Dashboard Récapitulatif (Nouvelle cellule)**

**Affiche automatiquement :**
```
📈 RÉSUMÉ DES EXÉCUTIONS MLFLOW
- Toutes les expériences créées
- Détails de chaque run
- Paramètres clés
- Métriques principales
```

## 📁 Fichiers créés

### 1. **MLFLOW_GUIDE.md** *(Guide complet)*
Documentation complète incluant :
- Vue d'ensemble
- Paramètres et métriques enregistrés
- Comment utiliser MLflow
- Structure du répertoire MLflow
- Résolution de problèmes

### 2. **mlflow_setup.py** *(Configuration centralisée)*
Script Python pour :
- Initialiser MLflow
- Créer les expériences
- Démarrer le serveur UI
- Afficher l'état des expériences

**Utilisation :**
```bash
python mlflow_setup.py
```

### 3. **start_mlflow_server.py** *(Lancement du serveur)*
Script autonome pour démarrer le serveur MLflow

**Utilisation :**
```bash
python start_mlflow_server.py
python start_mlflow_server.py --port 8080  # Port personnalisé
```

### 4. **mlflow.conf** *(Configuration)*
Fichier de configuration pour :
- URI du backend
- Noms des expériences
- Métriques à enregistrer
- Configuration du serveur

## 🚀 Flux d'utilisation

### Étape 1 : Exécuter le notebook
```bash
# En Colab ou Jupyter
# Exécutez toutes les cellules dans l'ordre
```

### Étape 2 : Vérifier les résultats
```python
# Le notebook affichera automatiquement :
✅ Données chargées et nettoyées
✅ Modèle A entraîné et évalué
✅ Métriques de classification
✅ Modèle B entraîné et évalué
✅ Métriques de régression
✅ Serveur MLflow lancé
✅ Dashboard récapitulatif
```

### Étape 3 : Accéder à MLflow UI
```
Ouvrir : http://localhost:5000
```

## 📊 Structures des données enregistrées

### Expérience 1 : Classification
```
Turbine_Failure_Prediction_Classification/
├── run_1/
│   ├── params/
│   │   ├── features
│   │   ├── target
│   │   ├── test_size
│   │   └── ...
│   ├── metrics/
│   │   ├── accuracy
│   │   ├── precision
│   │   ├── recall
│   │   ├── f1_score
│   │   └── roc_auc
│   └── artifacts/
│       ├── plots/
│       │   ├── confusion_matrix_model_a.html
│       │   └── roc_curve_model_a.html
│       └── classification_model/
```

### Expérience 2 : Régression
```
Turbine_Time_to_Failure_Prediction_Regression/
├── run_1/
│   ├── params/
│   │   ├── features
│   │   ├── target
│   │   ├── test_size_reg
│   │   └── ...
│   ├── metrics/
│   │   ├── mae
│   │   ├── mse
│   │   ├── rmse
│   │   └── r2_score
│   └── artifacts/
│       ├── plots/
│       │   ├── regression_predictions_plot.html
│       │   └── error_distribution.html
│       └── regression_model/
```

## 🎯 Points clés à retenir

### ✅ Conservation du code original
- Tous vos codes d'EDA, nettoyage et visualisation sont préservés
- Seul l'ajout de suivi MLflow a été effectué
- Aucun changement de logique métier

### ✅ Métriques intégrées
**Classification :**
- Accuracy, Precision, Recall, F1, ROC-AUC
- Matrice de confusion
- Courbe ROC

**Régression :**
- MAE, MSE, RMSE, R²
- Distribution des erreurs
- Scatter plot prédictions/réalité

### ✅ Suivi professionnel
- Noms de runs descriptifs
- Paramètres complets
- Artifacts téléchargeables
- Historique complètement traçable

## 🔍 Vérification de l'intégration

Après exécution du notebook, vous devriez voir :

```
✓ Fichier CSV chargé avec succès
✓ Données préparées pour classification
✓ [Classification Model] Tentative de chargement du modèle existant
✓ Nouveau modèle DecisionTreeClassifier entraîné
==================================================
ÉVALUATION DU MODÈLE A (CLASSIFICATION)
==================================================
Accuracy :           0.XXXX
Précision :          0.XXXX
Rappel (Recall) :    0.XXXX
F1-score :           0.XXXX
ROC-AUC Score :      0.XXXX
✓ Exécution MLflow enregistrée avec l'ID : <run_id>
...
[Régression - résultats similaires]
...
✓ Serveur MLflow démarré avec succès!
==================================================
🎯 ACCÈS À MLFLOW UI :
==================================================
En local : http://localhost:5000
```

## 📞 Support

### Besoin d'aide ?

1. **Consultez le guide MLflow** : `MLFLOW_GUIDE.md`
2. **Vérifiez la configuration** : `mlflow.conf`
3. **Lancez le serveur manuellement** : `python start_mlflow_server.py`

### Erreurs courantes

| Erreur | Solution |
|--------|----------|
| "Port 5000 déjà utilisé" | Changer le port avec `--port 8080` |
| "Répertoire mlruns introuvable" | Créé automatiquement, vérifier les permissions |
| "MLflow non installé" | `pip install mlflow` |

## ✨ Prochaines étapes recommandées

1. ✅ **Exécuter le notebook complet** - Voir tous les résultats
2. ✅ **Accéder à MLflow UI** - Explorer les visualisations
3. ✅ **Comparer les runs** - Analyser les différences de performance
4. ✅ **Exporter les modèles** - Préparer la production

## 📜 Version

- **Notebook** : ETL_MSPR2.ipynb
- **Adaptation MLflow** : v1.0
- **Date** : Février 2026
- **Statut** : ✅ Prêt pour la production

---

**Questions ?** Consultez `MLFLOW_GUIDE.md` pour plus de détails.
