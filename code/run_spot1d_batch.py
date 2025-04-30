import os
import subprocess
from multiprocessing import Pool

# Paths
fasta_dir = "data/fasta_files"
output_dir = "spot1d_outputs"
spot1d_script = "SPOT-1D-Single/spot1d_single.py"

# Make sure output directory exists
os.makedirs(output_dir, exist_ok=True)

def run_prediction(fasta_file):
    fasta_path = os.path.join(fasta_dir, fasta_file)

    print(f"⚡ Running {fasta_file}...")
    subprocess.run([
        "python", spot1d_script,
        "--file_list", fasta_path,
        "--save_path", output_dir   # ONLY folder now
    ])

if __name__ == "__main__":
    fasta_files = [f for f in os.listdir(fasta_dir) if f.endswith(".fasta")]

    # Parallelize
    num_processes = 12

    with Pool(num_processes) as pool:
        pool.map(run_prediction, fasta_files)
