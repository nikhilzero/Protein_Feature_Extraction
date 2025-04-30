import os
import numpy as np
import pandas as pd

def extract_pssm_sac(pssm_file, distance=10):
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
    if L <= distance or L < 5:
        return None

    segment_len = L // 5
    sac_vector = []

    for i in range(5):
        start = i * segment_len
        end = (i + 1) * segment_len if i < 4 else L
        segment = matrix[start:end]

        if segment.shape[0] <= distance:
            # Skip short segment
            sac_vector.extend([0] * 20)
            continue

        for col in range(20):
            values = segment[:, col]
            ac = np.mean(values[:-distance] * values[distance:])
            sac_vector.append(ac)

    return sac_vector

def process_directory(pssm_dir, output_csv):
    data = []
    for file in os.listdir(pssm_dir):
        if file.endswith('.pssm'):
            path = os.path.join(pssm_dir, file)
            features = extract_pssm_sac(path)
            if features:
                data.append([file.replace('.pssm', '')] + features)

    columns = ['Protein_ID'] + [f'SAC_{i+1}' for i in range(100)]
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(output_csv, index=False)

if __name__ == "__main__":
    process_directory("data/pssm_outputs", "features/pssm_sac.csv")
