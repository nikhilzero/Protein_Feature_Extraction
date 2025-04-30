import os
import pandas as pd
import numpy as np

# Define paths
spot1d_output_dir = "spot1d_outputs"
output_file = "features/torsion_composition.csv"

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

    if not set(["Phi", "Psi", "Theta", "Tau"]).issubset(df.columns):
        print(f"Warning: Missing torsion angle columns in {csv_file}. Skipping.")
        continue

    # Compute mean for each torsion angle
    mean_phi = np.mean(df["Phi"].values)
    mean_psi = np.mean(df["Psi"].values)
    mean_theta = np.mean(df["Theta"].values)
    mean_tau = np.mean(df["Tau"].values)

    feature_list.append([protein_id, mean_phi, mean_psi, mean_theta, mean_tau])

# Save to CSV
columns = ["Protein_ID", "Mean_Phi", "Mean_Psi", "Mean_Theta", "Mean_Tau"]
df_features = pd.DataFrame(feature_list, columns=columns)
df_features.to_csv(output_file, index=False)

print(f"Torsion Composition features extracted and saved to {output_file}")
