import pandas as pd
from pathlib import Path

# Base directory (assuming this script is in /features/)
base_dir = Path(__file__).parent

# File paths
merged_features_path = base_dir / 'merged_features.csv'
labels_path = base_dir / 'g_data.csv'
output_path = base_dir / 'final_training_data.csv'

# Load merged features
merged_features = pd.read_csv(merged_features_path)

# Load g_data.csv (labels) without header
labels = pd.read_csv(labels_path, header=None)

# Assign proper column names
labels.columns = ['Fold_no', 'Fold', 'Protein_ID', 'Protein']

# Strip whitespace from Protein_IDs
merged_features['Protein_ID'] = merged_features['Protein_ID'].str.strip()
labels['Protein_ID'] = labels['Protein_ID'].str.strip()

# Keep only relevant columns
labels = labels[['Protein_ID', 'Fold']]

# Merge by Protein_ID
final_data = pd.merge(merged_features, labels, on='Protein_ID', how='left')

# Save final training data
final_data.to_csv(output_path, index=False)

print(f"\n✅ Successfully merged! File created at: {output_path}")
