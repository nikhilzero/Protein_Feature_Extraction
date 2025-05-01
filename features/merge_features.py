import pandas as pd
import os

# Corrected Paths (DO NOT include 'Features/')
pssm_aao_path = 'pssm/pssm_aao.csv'
pssm_sd_path = 'pssm/pssm_sd.csv'
pssm_sac_path = 'pssm/pssm_sac.csv'

ss3_autocov_path = 'spot1d/ss3_autocov.csv'
torsion_comp_path = 'spot1d/torsion_composition.csv'
asa_bigram_path = 'spot1d/asa_bigram.csv'

# Load each feature file
pssm_aao = pd.read_csv(pssm_aao_path)
pssm_sd = pd.read_csv(pssm_sd_path)
pssm_sac = pd.read_csv(pssm_sac_path)

ss3_autocov = pd.read_csv(ss3_autocov_path)
torsion_comp = pd.read_csv(torsion_comp_path)
asa_bigram = pd.read_csv(asa_bigram_path)

# Merge all feature tables on 'Protein_ID'
merged_features = pssm_aao.merge(pssm_sd, on='Protein_ID') \
                           .merge(pssm_sac, on='Protein_ID') \
                           .merge(ss3_autocov, on='Protein_ID') \
                           .merge(torsion_comp, on='Protein_ID') \
                           .merge(asa_bigram, on='Protein_ID')

# Save the merged features
merged_output_file = 'merged_features.csv'
merged_features.to_csv(merged_output_file, index=False)

print(f"\n✅ Merged features saved successfully to: {merged_output_file}")
