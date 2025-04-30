import os
import pandas as pd
import numpy as np

# Define paths
spot1d_output_dir = "spot1d_outputs"
output_file = "features/ss3_autocov.csv"

# Make sure features directory exists
os.makedirs("features", exist_ok=True)

# List all Spot-1D CSV files
csv_files = [f for f in os.listdir(spot1d_output_dir) if f.endswith(".csv")]

# Prepare list to collect features
feature_list = []

# Process each protein CSV
for csv_file in csv_files:
    protein_id = os.path.splitext(csv_file)[0]
    csv_path = os.path.join(spot1d_output_dir, csv_file)

    # Load SPOT-1D output
    df = pd.read_csv(csv_path)

    if not set(["P3C", "P3H", "P3E"]).issubset(df.columns):
        print(f"Warning: Missing SS3 columns in {csv_file}. Skipping.")
        continue

    ss3_C = df["P3C"].values
    ss3_H = df["P3H"].values
    ss3_E = df["P3E"].values

    features = []

    for lag in range(1, 11):
        # Autocovariance for C, H, E at each lag
        for ss3_probs in [ss3_C, ss3_H, ss3_E]:
            if len(ss3_probs) > lag:
                acov = np.mean(ss3_probs[:-lag] * ss3_probs[lag:])
            else:
                acov = 0.0  # Short sequences, put 0
            features.append(acov)

    feature_list.append([protein_id] + features)

# Save to CSV
columns = ["Protein_ID"] + [f"SS3_ACOV_Lag{lag}_{state}" for lag in range(1, 11) for state in ["C", "H", "E"]]
df_features = pd.DataFrame(feature_list, columns=columns)
df_features.to_csv(output_file, index=False)

print(f"SS3 Autocovariance features extracted and saved to {output_file}")
