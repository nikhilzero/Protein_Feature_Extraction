import pandas as pd
import os

# Define base paths (relative to project root)
base_dir = os.path.dirname(__file__)  # current script location
pssm_dir = os.path.join(base_dir, 'pssm')
spot1d_dir = os.path.join(base_dir, 'spot1d')

# Paths to CSV files
pssm_aao_path = os.path.join(pssm_dir, 'pssm_aao.csv')
pssm_sd_path = os.path.join(pssm_dir, 'pssm_sd.csv')
pssm_sac_path = os.path.join(pssm_dir, 'pssm_sac.csv')

ss3_autocov_path = os.path.join(spot1d_dir, 'ss3_autocov.csv')
torsion_comp_path = os.path.join(spot1d_dir, 'torsion_composition.csv')
asa_bigram_path = os.path.join(spot1d_dir, 'asa_bigram.csv')

# Load CSVs
pssm_aao = pd.read_csv(pssm_aao_path)
pssm_sd = pd.read_csv(pssm_sd_path)
pssm_sac = pd.read_csv(pssm_sac_path)

ss3_autocov = pd.read_csv(ss3_autocov_path)
torsion_comp = pd.read_csv(torsion_comp_path)
asa_bigram = pd.read_csv(asa_bigram_path)

# Merge all features on Protein_ID
merged_features = pssm_aao.merge(pssm_sd, on='Protein_ID') \
                           .merge(pssm_sac, on='Protein_ID') \
                           .merge(ss3_autocov, on='Protein_ID') \
                           .merge(torsion_comp, on='Protein_ID') \
                           .merge(asa_bigram, on='Protein_ID')

# Save output to project root
output_path = os.path.join(base_dir, 'merged_features.csv')
merged_features.to_csv(output_path, index=False)

print(f"\n✅ Merged features saved successfully to: {output_path}")
