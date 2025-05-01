import pandas as pd

# Load merged features
merged_features = pd.read_csv('merged_features.csv')

# Load labels.csv without header
labels = pd.read_csv('g_data.csv', header=None)

# Assign 4 column names
labels.columns = ['Fold_no', 'Fold', 'Protein_ID', 'Protein']

# Clean Protein_IDs
merged_features['Protein_ID'] = merged_features['Protein_ID'].str.strip()
labels['Protein_ID'] = labels['Protein_ID'].str.strip()

# Only keep Protein_ID and Fold for merging
labels = labels[['Protein_ID', 'Fold']]

# Merge
final_data = pd.merge(merged_features, labels, on='Protein_ID', how='left')

# Save
final_data.to_csv('final_training_data.csv', index=False)

print("\n✅ Successfully merged! final_training_data.csv created.")
