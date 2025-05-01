import os
import numpy as np
import pandas as pd

# 🔍 Function to extract Standard Deviation (mean per segment) from a single PSSM file
def extract_pssm_sd(pssm_file):
    matrix = []

    # Step 1: Parse the PSSM file and extract 20 PSSM columns per line
    with open(pssm_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 22 and parts[0].isdigit():
                try:
                    values = list(map(int, parts[2:22]))  # 20 values per amino acid position
                    if len(values) == 20:
                        matrix.append(values)
                except:
                    continue  # Skip lines with non-numeric values

    if not matrix:
        return None  # Skip empty matrix

    matrix = np.array(matrix)
    L = matrix.shape[0]  # Sequence length
    if L < 4:
        return None  # Skip too-short sequences

    # Step 2: Divide matrix into 4 segments
    segment_length = L // 4
    sd_vector = []

    for i in range(4):
        start = i * segment_length
        end = (i + 1) * segment_length if i < 3 else L  # Last segment includes any remainder
        segment = matrix[start:end]

        # Step 3: Compute mean for each column (20 amino acids) in the segment
        avg = np.mean(segment, axis=0)
        sd_vector.extend(avg)  # Append 20 mean values per segment → total 80 features

    return sd_vector

# 🗂️ Process all .pssm files in a directory and extract features
def process_directory(pssm_dir, output_csv):
    data = []

    for file in os.listdir(pssm_dir):
        if file.endswith('.pssm'):
            path = os.path.join(pssm_dir, file)
            features = extract_pssm_sd(path)
            if features:
                data.append([file.replace('.pssm', '')] + features)

    # Column names for output CSV
    columns = ['Protein_ID'] + [f'SD_{i+1}' for i in range(80)]
    df = pd.DataFrame(data, columns=columns)

    # Save the extracted features to CSV
    df.to_csv(output_csv, index=False)

# 🚀 Entry point
if __name__ == "__main__":
    # Folder with PSSM files and output CSV path
    process_directory("data/pssm_outputs", "features/pssm_sd.csv")
