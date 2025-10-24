import pandas as pd
import os
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(
        description="Analyse les fichiers CSV pour détecter les colonnes contenant des valeurs NaN."
    )
    parser.add_argument(
        "--data-dir",
        required=True,
        help="Chemin vers le dossier contenant les fichiers CSV."
    )
    parser.add_argument(
        "--output",
        default="rapport_nan_par_dataset.csv",
        help="Chemin de sortie du rapport CSV (par défaut: rapport_nan_par_dataset.csv)."
    )

    args = parser.parse_args()

    data_dir = args.data_dir
    output_path = args.output

    if not os.path.exists(data_dir):
        print(f"❌ Erreur : le dossier '{data_dir}' n'existe pas.")
        sys.exit(1)

    results = []

    for file_name in os.listdir(data_dir):
        if file_name.endswith(".csv"):
            file_path = os.path.join(data_dir, file_name)
            print(f"🔍 Analyse de {file_name} ...")

            try:
                # Lecture du CSV (auto-détection du séparateur)
                # keep_default_na=False empêche de traiter les cellules vides comme NaN
                # On spécifie explicitement quelles valeurs sont considérées comme NaN
                df = pd.read_csv(
                    file_path, 
                    sep=None, 
                    engine="python",
                    keep_default_na=False,
                    na_values=['nan', 'NaN', 'NAN', 'null', 'NULL', 'None', 'N/A', 'n/a', '#N/A']
                )

                # Nombre total de lignes
                total_rows = len(df)

                # Colonnes contenant au moins un NaN (valeurs vraiment NaN, pas les chaînes vides)
                nan_columns = df.columns[df.isna().any()].tolist()

                # Comptage des NaN par colonne
                nan_counts = df.isna().sum()[df.isna().sum() > 0].to_dict()

                # Ajouter tous les datasets (avec ou sans NaN)
                if nan_columns:
                    results.append({
                        "dataset": file_name,
                        "total_row_count": total_rows,
                        "has_nan": "OUI ❌",
                        "nan_columns": ", ".join(nan_columns),
                        "nan_counts": str(nan_counts)
                    })
                else:
                    results.append({
                        "dataset": file_name,
                        "total_row_count": total_rows,
                        "has_nan": "NON ✓",
                        "nan_columns": "",
                        "nan_counts": ""
                    })

            except Exception as e:
                print(f"⚠️ Erreur lors de la lecture de {file_name}: {e}")

    if not results:
        print("✅ Aucun fichier CSV trouvé.")
        sys.exit(0)

    # 📊 Génération du rapport global
    report_df = pd.DataFrame(results)
    
    # Statistiques
    total_files = len(results)
    files_with_nan = len([r for r in results if r['has_nan'] == "OUI ❌"])
    files_without_nan = total_files - files_with_nan
    
    print(f"\n{'='*60}")
    print(f"📊 RÉSUMÉ")
    print(f"{'='*60}")
    print(f"Fichiers analysés: {total_files}")
    print(f"Fichiers avec NaN: {files_with_nan}")
    print(f"Fichiers sans NaN: {files_without_nan}")
    
    print("\n=== Rapport complet des datasets ===")
    print(report_df.to_string(index=False))

    # 💾 Export CSV
    report_df.to_csv(output_path, index=False)
    print(f"\n✅ Rapport exporté dans : {output_path}")


if __name__ == "__main__":
    main()
