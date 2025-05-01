import pandas as pd
from pathlib import Path

# Set base directory (assuming this script is in /features/)
base_dir = Path(__file__).parent

# File paths
raw_g_data_path = base_dir / 'g_data.csv'
clean_labels_path = base_dir / 'labels.csv'

# Load messy g_data file
g_data = pd.read_csv(raw_g_data_path)

# Initialize lists for Protein_IDs and Folds
protein_ids = []
folds = []

# Parse column headers to extract protein IDs and their corresponding fold types
for col in g_data.columns:
    if col.startswith('>'):
        protein_id = col[1:].strip()
        protein_ids.append(protein_id)
        folds.append(g_data[col].iloc[0])  # First row typically has the fold label

# Create cleaned DataFrame
labels_df = pd.DataFrame({
    'Protein_ID': protein_ids,
    'Fold': folds
})

# Save to labels.csv
labels_df.to_csv(clean_labels_path, index=False)

print(f"\n✅ Clean labels.csv created at: {clean_labels_path}")
