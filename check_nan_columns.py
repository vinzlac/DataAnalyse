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
                df = pd.read_csv(file_path, sep=None, engine="python")

                # Colonnes contenant au moins un NaN
                nan_columns = df.columns[df.isna().any()].tolist()

                # Comptage des NaN par colonne
                nan_counts = df.isna().sum()[df.isna().sum() > 0].to_dict()

                results.append({
                    "dataset": file_name,
                    "nan_columns": ", ".join(nan_columns),
                    "nan_counts": nan_counts
                })

            except Exception as e:
                print(f"⚠️ Erreur lors de la lecture de {file_name}: {e}")

    if not results:
        print("✅ Aucun fichier avec des NaN détecté ou aucun CSV trouvé.")
        sys.exit(0)

    # 📊 Génération du rapport global
    report_df = pd.DataFrame(results)
    print("\n=== Colonnes contenant au moins un NaN ===")
    print(report_df)

    # 💾 Export CSV
    report_df.to_csv(output_path, index=False)
    print(f"\n✅ Rapport exporté dans : {output_path}")


if __name__ == "__main__":
    main()
