import pandas as pd

# Load the messy g_data
g_data = pd.read_csv('g_data.csv')

# Check the first few rows to understand structure
print(g_data.head())

# Create a clean DataFrame

protein_ids = []
folds = []

# Each row has messed up headers, so we need to parse manually
for col in g_data.columns:
    if col.startswith('>'):
        # Remove '>' symbol
        protein_id = col[1:]
        protein_ids.append(protein_id)
        folds.append(g_data[col].iloc[0])  # take the first value (maybe the fold name or type)

# Now create clean DataFrame
labels_df = pd.DataFrame({
    'Protein_ID': protein_ids,
    'Fold': folds
})

# Save it
labels_df.to_csv('labels.csv', index=False)

print("\n✅ Clean labels.csv created successfully!")
