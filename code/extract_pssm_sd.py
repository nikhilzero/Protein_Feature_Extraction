import os
import numpy as np
import pandas as pd

def extract_pssm_sd(pssm_file):
    matrix = []
    with open(pssm_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 22 and parts[0].isdigit():
                try:
                    values = list(map(int, parts[2:22]))
                    if len(values) == 20:
                        matrix.append(values)
                except:
                    continue
    if not matrix:
        return None

    matrix = np.array(matrix)
    L = matrix.shape[0]
    if L < 4:
        return None

    # Split into 4 segments
    segment_length = L // 4
    sd_vector = []
    for i in range(4):
        start = i * segment_length
        end = (i + 1) * segment_length if i < 3 else L
        segment = matrix[start:end]
        avg = np.mean(segment, axis=0)
        sd_vector.extend(avg)

    return sd_vector

def process_directory(pssm_dir, output_csv):
    data = []
    for file in os.listdir(pssm_dir):
        if file.endswith('.pssm'):
            path = os.path.join(pssm_dir, file)
            features = extract_pssm_sd(path)
            if features:
                data.append([file.replace('.pssm', '')] + features)

    columns = ['Protein_ID'] + [f'SD_{i+1}' for i in range(80)]
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(output_csv, index=False)

if __name__ == "__main__":
    process_directory("data/pssm_outputs", "features/pssm_sd.csv")
