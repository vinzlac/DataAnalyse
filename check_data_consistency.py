import pandas as pd
import os
import argparse
import sys
from datetime import datetime
import re

def detect_value_type(value):
    """
    Détecte le type d'une valeur.
    Retourne: 'number', 'date', 'string', ou 'nan'
    """
    if pd.isna(value):
        return 'nan'
    
    # Convertir en string pour l'analyse
    str_value = str(value).strip()
    
    if str_value == '':
        return 'empty'
    
    # Test 1: Est-ce un nombre ?
    try:
        float(str_value)
        return 'number'
    except ValueError:
        pass
    
    # Test 2: Est-ce une date ? (plusieurs formats courants)
    date_formats = [
        '%Y-%m-%d',           # 2023-12-25
        '%d/%m/%Y',           # 25/12/2023
        '%m/%d/%Y',           # 12/25/2023
        '%Y/%m/%d',           # 2023/12/25
        '%d-%m-%Y',           # 25-12-2023
        '%Y-%m-%d %H:%M:%S',  # 2023-12-25 14:30:00
        '%d/%m/%Y %H:%M:%S',  # 25/12/2023 14:30:00
        '%Y-%m-%dT%H:%M:%S',  # ISO format
        '%Y-%m-%dT%H:%M:%SZ', # ISO format with Z
        '%d.%m.%Y',           # 25.12.2023
        '%Y.%m.%d',           # 2023.12.25
    ]
    
    for date_format in date_formats:
        try:
            datetime.strptime(str_value, date_format)
            return 'date'
        except ValueError:
            continue
    
    # Test 3: Pattern de date plus flexible (YYYY, MM, DD présents)
    # Exemple: "2023-12-25" ou variations
    date_pattern = r'(\d{4}[-/\.]\d{1,2}[-/\.]\d{1,2})|(\d{1,2}[-/\.]\d{1,2}[-/\.]\d{4})'
    if re.match(date_pattern, str_value):
        return 'date'
    
    # Sinon, c'est une string
    return 'string'


def analyze_column_consistency(series):
    """
    Analyse la cohérence des types dans une série pandas.
    Retourne un dictionnaire avec les informations de cohérence.
    """
    # Compter les types de valeurs (en excluant les NaN)
    type_counts = {}
    total_values = 0
    nan_count = 0
    
    for value in series:
        value_type = detect_value_type(value)
        
        if value_type == 'nan':
            nan_count += 1
        elif value_type == 'empty':
            continue  # On ignore les valeurs vides
        else:
            total_values += 1
            type_counts[value_type] = type_counts.get(value_type, 0) + 1
    
    # Déterminer si la colonne est cohérente
    unique_types = list(type_counts.keys())
    is_consistent = len(unique_types) <= 1
    
    # Type dominant (excluant NaN)
    dominant_type = None
    if unique_types:
        dominant_type = max(type_counts, key=type_counts.get)
    
    # Si on a des NaN et un seul autre type, supposer que les NaN devraient être de ce type
    expected_type = dominant_type
    if dominant_type and nan_count > 0:
        # Les NaN sont probablement du même type que le type dominant
        pass
    
    return {
        'is_consistent': is_consistent,
        'types_found': unique_types,
        'type_counts': type_counts,
        'dominant_type': dominant_type,
        'total_values': total_values,
        'nan_count': nan_count,
        'inconsistency_details': None if is_consistent else f"Mélange de types: {', '.join([f'{t}({type_counts[t]})' for t in unique_types])}"
    }


def main():
    parser = argparse.ArgumentParser(
        description="Vérifie la cohérence des types de données dans les colonnes des fichiers CSV."
    )
    parser.add_argument(
        "--data-dir",
        required=True,
        help="Chemin vers le dossier contenant les fichiers CSV."
    )
    parser.add_argument(
        "--output",
        default="rapport_coherence_donnees.csv",
        help="Chemin de sortie du rapport CSV (par défaut: rapport_coherence_donnees.csv)."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Affiche les détails des colonnes cohérentes également."
    )

    args = parser.parse_args()

    data_dir = args.data_dir
    output_path = args.output
    verbose = args.verbose

    if not os.path.exists(data_dir):
        print(f"❌ Erreur : le dossier '{data_dir}' n'existe pas.")
        sys.exit(1)

    results = []
    total_files = 0
    total_inconsistencies = 0

    for file_name in os.listdir(data_dir):
        if file_name.endswith(".csv"):
            total_files += 1
            file_path = os.path.join(data_dir, file_name)
            print(f"\n🔍 Analyse de {file_name} ...")

            try:
                # Lecture du CSV (auto-détection du séparateur)
                df = pd.read_csv(file_path, sep=None, engine="python")
                
                # Nombre total de lignes
                total_rows = len(df)
                
                file_inconsistencies = 0
                
                for column in df.columns:
                    analysis = analyze_column_consistency(df[column])
                    
                    # Ne rapporter que les incohérences, sauf si verbose
                    if not analysis['is_consistent']:
                        file_inconsistencies += 1
                        total_inconsistencies += 1
                        
                        results.append({
                            "fichier": file_name,
                            "total_row_count": total_rows,
                            "colonne": column,
                            "coherent": "NON ❌",
                            "types_detectes": ", ".join(analysis['types_found']),
                            "type_dominant": analysis['dominant_type'] or "N/A",
                            "details": analysis['inconsistency_details'],
                            "nb_valeurs": analysis['total_values'],
                            "nb_nan": analysis['nan_count']
                        })
                        
                        print(f"  ⚠️  Colonne '{column}': {analysis['inconsistency_details']}")
                    
                    elif verbose:
                        results.append({
                            "fichier": file_name,
                            "total_row_count": total_rows,
                            "colonne": column,
                            "coherent": "OUI ✓",
                            "types_detectes": ", ".join(analysis['types_found']) if analysis['types_found'] else "vide",
                            "type_dominant": analysis['dominant_type'] or "N/A",
                            "details": "Cohérent",
                            "nb_valeurs": analysis['total_values'],
                            "nb_nan": analysis['nan_count']
                        })
                
                if file_inconsistencies == 0:
                    print(f"  ✅ Toutes les colonnes sont cohérentes ({len(df.columns)} colonnes analysées)")

            except Exception as e:
                print(f"⚠️ Erreur lors de la lecture de {file_name}: {e}")

    # Résumé
    print(f"\n{'='*60}")
    print(f"📊 RÉSUMÉ")
    print(f"{'='*60}")
    print(f"Fichiers analysés: {total_files}")
    print(f"Incohérences détectées: {total_inconsistencies}")
    
    if not results:
        print("\n✅ Aucune incohérence détectée ou aucun CSV trouvé.")
        sys.exit(0)

    # 📊 Génération du rapport
    report_df = pd.DataFrame(results)
    
    if not verbose and total_inconsistencies > 0:
        print(f"\n=== Colonnes avec incohérences de types ===")
        print(report_df.to_string(index=False))
    elif verbose:
        print(f"\n=== Rapport complet (toutes les colonnes) ===")
        print(report_df.to_string(index=False))

    # 💾 Export CSV
    report_df.to_csv(output_path, index=False)
    print(f"\n✅ Rapport exporté dans : {output_path}")


if __name__ == "__main__":
    main()

