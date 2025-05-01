import os
import numpy as np
import pandas as pd

# 🔍 Function to extract SAC features from a single PSSM file
def extract_pssm_sac(pssm_file, distance=10):
    matrix = []

    # Step 1: Parse valid PSSM rows (20 columns per amino acid position)
    with open(pssm_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 22 and parts[0].isdigit():
                try:
                    values = list(map(int, parts[2:22]))  # 20 features
                    if len(values) == 20:
                        matrix.append(values)
                except:
                    continue  # skip if conversion fails

    if not matrix:
        return None  # Skip empty files

    matrix = np.array(matrix)
    L = matrix.shape[0]  # Protein length
    if L <= distance or L < 5:
        return None  # Not enough length to compute SAC

    # Step 2: Segment the protein into 5 equal parts
    segment_len = L // 5
    sac_vector = []

    for i in range(5):
        start = i * segment_len
        end = (i + 1) * segment_len if i < 4 else L  # Last segment includes remainder
        segment = matrix[start:end]

        if segment.shape[0] <= distance:
            # Pad with zeros if segment too short
            sac_vector.extend([0] * 20)
            continue

        # Step 3: Compute autocovariance for each column
        for col in range(20):
            values = segment[:, col]
            # Mean of product of values with a lag of 'distance'
            ac = np.mean(values[:-distance] * values[distance:])
            sac_vector.append(ac)

    return sac_vector  # Length = 5 segments × 20 = 100 features

# 🗃️ Function to process a folder of PSSM files
def process_directory(pssm_dir, output_csv):
    data = []

    for file in os.listdir(pssm_dir):
        if file.endswith('.pssm'):
            path = os.path.join(pssm_dir, file)
            features = extract_pssm_sac(path)
            if features:
                data.append([file.replace('.pssm', '')] + features)

    # Step 4: Save as DataFrame
    columns = ['Protein_ID'] + [f'SAC_{i+1}' for i in range(100)]
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(output_csv, index=False)

# 🚀 Entry point for script
if __name__ == "__main__":
    # Directory where .pssm files are stored and output location
    process_directory("data/pssm_outputs", "features/pssm_sac.csv")
