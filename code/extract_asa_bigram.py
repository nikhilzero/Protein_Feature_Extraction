import os
import pandas as pd
import numpy as np

# Define paths
spot1d_output_dir = "spot1d_outputs"
output_file = "features/asa_bigram.csv"

# Make sure features directory exists
os.makedirs("features", exist_ok=True)

# List all SPOT-1D CSV files
csv_files = [f for f in os.listdir(spot1d_output_dir) if f.endswith(".csv")]

# Prepare list to collect features
feature_list = []

# Process each protein CSV
for csv_file in csv_files:
    protein_id = os.path.splitext(csv_file)[0]
    csv_path = os.path.join(spot1d_output_dir, csv_file)

    # Load SPOT-1D output
    df = pd.read_csv(csv_path)

    if "ASA" not in df.columns:
        print(f"Warning: ASA column missing in {csv_file}. Skipping.")
        continue

    asa_values = df["ASA"].values

    if len(asa_values) < 3:
        print(f"Warning: Not enough residues in {csv_file}. Skipping.")
        continue

    # Compute ASA bigram feature: ASA[i] * ASA[i+2] average
    asa_bigram = np.mean(asa_values[:-2] * asa_values[2:])

    feature_list.append([protein_id, asa_bigram])

# Save to CSV
df_features = pd.DataFrame(feature_list, columns=["Protein_ID", "ASA_Bigram"])
df_features.to_csv(output_file, index=False)

print(f"ASA Bigram features extracted and saved to {output_file}")
