# DataAnalyse - Analyse de qualité des données CSV

## Description

Cette suite d'outils analyse les fichiers CSV d'un répertoire pour détecter des problèmes de qualité de données :
- **check_nan_columns.py** : Détecte les colonnes contenant des valeurs NaN (valeurs manquantes)
- **check_data_consistency.py** : Vérifie la cohérence des types de données dans les colonnes

## Fonctionnalités

### check_nan_columns.py
- 🔍 Scan automatique de tous les fichiers CSV d'un répertoire
- 📊 Détection des colonnes contenant au moins une valeur NaN
- 📈 Comptage du nombre de valeurs NaN par colonne
- 💾 Export des résultats dans un fichier CSV de rapport

### check_data_consistency.py
- 🔍 Analyse des types de données dans chaque colonne
- ⚠️ Détection des incohérences (mélange de nombres/dates/strings)
- 📊 Identification du type dominant dans chaque colonne
- 📈 Comptage des occurrences de chaque type
- 💾 Rapport détaillé des colonnes incohérentes

### Commun
- ⚙️ Détection automatique du séparateur CSV (`,`, `;`, `\t`, etc.)
- 🎯 Gestion robuste des erreurs

## Prérequis

- Python 3.7 ou supérieur
- pip (gestionnaire de paquets Python)

## Installation

1. Clonez ou téléchargez ce dépôt

2. Installez les dépendances :

**Sur la plupart des systèmes :**
```bash
pip install -r requirements.txt
```

**Sur macOS avec Python 3.13+ (environnement géré par Homebrew) :**
```bash
pip3 install --user --break-system-packages -r requirements.txt
```

**Alternative avec environnement virtuel (recommandé) :**
```bash
python3 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Utilisation

### 1️⃣ Détection des valeurs NaN (check_nan_columns.py)

#### Syntaxe de base

```bash
python check_nan_columns.py --data-dir ./input --output ./output/rapport_nan.csv
```

#### Paramètres

| Paramètre | Description | Obligatoire | Valeur par défaut |
|-----------|-------------|-------------|-------------------|
| `--data-dir` | Chemin vers le dossier contenant les fichiers CSV | ✅ Oui | - |
| `--output` | Chemin de sortie du rapport CSV | ❌ Non | `rapport_nan_par_dataset.csv` |

#### Exemples

```bash
# Analyse basique avec sortie par défaut
python check_nan_columns.py --data-dir ./input

# Analyse avec fichier de rapport personnalisé
python check_nan_columns.py --data-dir ./input --output ./output/rapport_nan.csv
```

---

### 2️⃣ Vérification de la cohérence des types (check_data_consistency.py)

#### Syntaxe de base

```bash
python check_data_consistency.py --data-dir ./input --output ./output/rapport_coherence.csv
```

#### Paramètres

| Paramètre | Description | Obligatoire | Valeur par défaut |
|-----------|-------------|-------------|-------------------|
| `--data-dir` | Chemin vers le dossier contenant les fichiers CSV | ✅ Oui | - |
| `--output` | Chemin de sortie du rapport CSV | ❌ Non | `rapport_coherence_donnees.csv` |
| `--verbose` | Affiche aussi les colonnes cohérentes | ❌ Non | `False` |

#### Exemples

```bash
# Analyse basique (affiche uniquement les incohérences)
python check_data_consistency.py --data-dir ./input

# Analyse avec rapport personnalisé
python check_data_consistency.py --data-dir ./input --output ./output/coherence.csv

# Analyse verbose (affiche toutes les colonnes)
python check_data_consistency.py --data-dir ./input --verbose
```

#### Types de données détectés

Le script détecte automatiquement :
- **number** : Nombres entiers ou décimaux (int, float)
- **date** : Dates dans différents formats (YYYY-MM-DD, DD/MM/YYYY, etc.)
- **string** : Chaînes de caractères textuelles
- **nan** : Valeurs manquantes (ignorées pour l'analyse de cohérence)

#### Exemples d'incohérences détectées

- ✅ Colonne avec uniquement des nombres → **Cohérent**
- ✅ Colonne avec nombres + NaN → **Cohérent** (NaN ignoré)
- ❌ Colonne avec nombres + strings → **Incohérent**
- ❌ Colonne avec dates + strings → **Incohérent**
- ❌ Colonne avec dates + nombres → **Incohérent**

## Format des rapports

### Rapport NaN (check_nan_columns.py)

Colonnes du rapport CSV :

| Colonne | Description |
|---------|-------------|
| `dataset` | Nom du fichier CSV analysé |
| `total_row_count` | Nombre total de lignes dans le dataset |
| `nan_columns` | Liste des colonnes contenant des valeurs NaN (séparées par des virgules) |
| `nan_counts` | Dictionnaire avec le nombre de NaN par colonne |

Exemple :
```csv
dataset,total_row_count,nan_columns,nan_counts
data1.csv,100,"age, salary","{'age': 5, 'salary': 3}"
data2.csv,50,address,"{'address': 12}"
```

### Rapport de cohérence (check_data_consistency.py)

Colonnes du rapport CSV :

| Colonne | Description |
|---------|-------------|
| `fichier` | Nom du fichier CSV analysé |
| `colonne` | Nom de la colonne analysée |
| `coherent` | OUI ✓ ou NON ❌ |
| `types_detectes` | Liste des types trouvés (number, date, string) |
| `type_dominant` | Type le plus fréquent dans la colonne |
| `details` | Description de l'incohérence ou "Cohérent" |
| `nb_valeurs` | Nombre de valeurs non-NaN |
| `nb_nan` | Nombre de valeurs NaN |

Exemple :
```csv
fichier,colonne,coherent,types_detectes,type_dominant,details,nb_valeurs,nb_nan
data1.csv,price,NON ❌,"number, string",number,"Mélange de types: number(95), string(5)",100,0
data1.csv,date,OUI ✓,date,date,Cohérent,100,0
```

## Structure du projet

```
DataAnalyse/
├── check_nan_columns.py       # Script de détection des valeurs NaN
├── check_data_consistency.py  # Script de vérification de cohérence des types
├── requirements.txt            # Dépendances Python
├── README.md                   # Documentation
├── .gitignore                  # Fichiers à ignorer par Git
├── venv/                       # Environnement virtuel (généré)
├── input/                      # Dossier pour les CSV sources (ignoré par Git)
└── output/                     # Dossier pour les rapports (ignoré par Git)
```

## Gestion des erreurs

Les scripts gèrent les cas suivants :
- ✅ Répertoire inexistant : affiche un message d'erreur et quitte
- ✅ Fichiers CSV corrompus : affiche un avertissement et continue
- ✅ Aucun fichier CSV trouvé : affiche un message et quitte normalement
- ✅ Aucune anomalie détectée : affiche un message et quitte normalement

## Aide

Pour afficher l'aide de chaque script :
```bash
python check_nan_columns.py --help
python check_data_consistency.py --help
```

## Licence

Ce projet est fourni tel quel sans garantie.
