import pandas as pd
import os

# Load without header (header=None)
df = pd.read_csv("data/g_data.csv", header=None)

# Pick only the correct two columns
df = df[[df.columns[2], df.columns[3]]]

# Rename the columns
df.columns = ['Header', 'Sequence']

# Clean '>'
df['Protein_ID'] = df['Header'].str.replace('>', '', regex=False)

# Rearranging
df = df[['Protein_ID', 'Sequence']]

# Write out fasta files
output_dir = "data/fasta_files"
os.makedirs(output_dir, exist_ok=True)

for index, row in df.iterrows():
    fasta_content = f">{row['Protein_ID']}\n{row['Sequence']}\n"
    with open(os.path.join(output_dir, f"{row['Protein_ID']}.fasta"), "w") as f:
        f.write(fasta_content)
