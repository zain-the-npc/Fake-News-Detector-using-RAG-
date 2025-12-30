import pandas as pd
from pathlib import Path

def preprocess_liar():
    print("🔄 Starting LIAR dataset preprocessing...")

    # Define paths
    base_path = Path("data/liar")
    processed_path = Path("data/processed")
    processed_path.mkdir(parents=True, exist_ok=True)

    # Define columns as per LIAR dataset documentation
    cols = [
        "id", "label", "statement", "subject", "speaker", "speaker_job",
        "state_info", "party", "barely_true_ct", "false_ct", "half_true_ct",
        "mostly_true_ct", "pants_fire_ct", "context"
    ]

    # ✅ Read the TSV files
    try:
        train = pd.read_csv(base_path / "train.tsv", sep="\t", header=None, names=cols)
        test = pd.read_csv(base_path / "test.tsv", sep="\t", header=None, names=cols)
        valid = pd.read_csv(base_path / "valid.tsv", sep="\t", header=None, names=cols)
        print("📂 Loaded train, test, and valid files successfully.")
    except FileNotFoundError:
        print("❌ One or more LIAR files (train.tsv, test.tsv, valid.tsv) not found in data/liar/")
        return

    # ✅ Combine all splits into one DataFrame
    df = pd.concat([train, test, valid], ignore_index=True)
    print(f"📊 Combined dataset shape: {df.shape}")

    # ✅ Map multi-level labels to binary real/fake
    real_labels = ["true", "mostly-true"]
    df["binary_label"] = df["label"].apply(lambda x: "real" if x in real_labels else "fake")

    # ✅ Keep only relevant columns
    df_clean = df[["statement", "binary_label", "speaker", "context"]].dropna().reset_index(drop=True)

    # ✅ Save to processed folder
    output_file = processed_path / "liar_clean.csv"
    df_clean.to_csv(output_file, index=False, encoding="utf-8")

    print(f"✅ Preprocessing complete! Saved cleaned file to: {output_file}")
    print(df_clean.head())

if __name__ == "__main__":
    preprocess_liar()
