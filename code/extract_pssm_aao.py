import os
import numpy as np
import pandas as pd

def extract_pssm_aao(pssm_file):
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
    mat = np.array(matrix)
    return np.sum(mat, axis=0).tolist()  # shape (20,)

def process_directory(pssm_dir, output_csv):
    data = []
    for file in os.listdir(pssm_dir):
        if file.endswith('.pssm'):
            path = os.path.join(pssm_dir, file)
            features = extract_pssm_aao(path)
            if features:
                data.append([file.replace('.pssm', '')] + features)

    columns = ['Protein_ID'] + [f'AAO_{i+1}' for i in range(20)]
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(output_csv, index=False)

if __name__ == "__main__":
    process_directory("data/pssm_outputs", "features/pssm_aao.csv")
