import os
import numpy as np
import pandas as pd

# 🔍 Function to extract AAO features from a single PSSM file
def extract_pssm_aao(pssm_file):
    matrix = []
    with open(pssm_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            # Ensure this line represents a valid row in the PSSM matrix
            if len(parts) >= 22 and parts[0].isdigit():
                try:
                    # Extract 20 PSSM values (columns 3 to 22)
                    values = list(map(int, parts[2:22]))
                    if len(values) == 20:
                        matrix.append(values)
                except:
                    continue  # skip malformed lines
    if not matrix:
        return None  # return None if matrix is empty
    mat = np.array(matrix)
    return np.sum(mat, axis=0).tolist()  # Sum column-wise (20 features)

# 🗃️ Function to process a folder full of .pssm files
def process_directory(pssm_dir, output_csv):
    data = []

    # Loop through all files in the directory
    for file in os.listdir(pssm_dir):
        if file.endswith('.pssm'):
            path = os.path.join(pssm_dir, file)
            features = extract_pssm_aao(path)
            if features:
                # Add Protein_ID (from filename) + 20 feature values
                data.append([file.replace('.pssm', '')] + features)

    # Prepare column names
    columns = ['Protein_ID'] + [f'AAO_{i+1}' for i in range(20)]

    # Create and save DataFrame
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(output_csv, index=False)

# 🚀 Entry point
if __name__ == "__main__":
    # Folder containing PSSM files and output CSV location
    process_directory("data/pssm_outputs", "features/pssm_aao.csv")
