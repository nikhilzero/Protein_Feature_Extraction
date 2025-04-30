# ML_Final_Project: Protein Feature Extraction Pipeline

This project builds a clean and reproducible pipeline to extract PSSM and structural features from protein sequences, starting only from `g_data.csv`.

---

## Step 1: FASTA File Preparation

- Input: `g_data.csv` inside the `data/` directory.
- Goal: Generate individual `.fasta` files, one per protein.

### Handling Invalid Amino Acids ('U' → 'X')

**Problem:**  
The original `g_data.csv` contained the amino acid `'U'` (Selenocysteine), which causes errors in:
- SPOT-1D
- PSI-BLAST
- PSSM matrix generation

**Solution:**  
- Manually replaced all occurrences of `'U'` with `'X'` directly in `g_data.csv`.
- Then generated `.fasta` files.

---

## Step 2: SwissProt BLAST Database Setup

- Downloaded SwissProt database (`uniprot_sprot.fasta`) from UniProt FTP.
- Unzipped the database.
- Created a BLAST+ database using:

```bash
makeblastdb -in uniprot_sprot.fasta -dbtype prot
```

---

## Step 3: PSSM Matrix Generation (PSI-BLAST)

- Ran PSI-BLAST (`psiblast`) for each `.fasta` file inside `data/fasta_files/`.
- Used the SwissProt BLAST database prepared earlier.
- Settings used:
  - Number of iterations: 3
  - E-value cutoff: 0.001
- Saved the output `.pssm` files inside the `pssm_outputs/` folder.

**Command used to run multiple PSI-BLAST jobs in parallel:**

```bash
bash code/run_psiblast.sh
```

---

## Step 4: PSSM Feature Extraction

After generating `.pssm` files from PSI-BLAST, the following features were extracted:

| Feature Set                             | Number of Features |
|:-----------------------------------------|:------------------:|
| PSSM-AAO (Amino Acid Occurrence)          | 20 |
| PSSM-SD (Standard Deviation over Segments)| 80 |
| PSSM-SAC (Sequence Autocovariance)        | 100 |

Each `.pssm` file was processed using the following scripts:

- `code/extract_pssm_aao.py` → outputs `features/pssm_aao.csv`
- `code/extract_pssm_sd.py` → outputs `features/pssm_sd.csv`
- `code/extract_pssm_sac.py` → outputs `features/pssm_sac.csv`

### Details:
- **PSSM-AAO**: Summation of scores across all amino acids.
- **PSSM-SD**: Mean and standard deviation values across 4 segments.
- **PSSM-SAC**: Autocovariance of scores across 5 segments with a lag of 10.

---

## Step 5: SPOT-1D-Single Structural Prediction

- Cloned SPOT-1D-Single into the `SPOT-1D-Single/` folder.
- Downloaded and extracted pre-trained models and standardization files (`means_single.pkl`, `stds_single.pkl`).
- Modified SPOT-1D-Single to:
  - Accept `.fasta` file paths directly.
  - Output predictions into the `spot1d_outputs/` folder.

### Notes:
- Always pass the **output folder** (`spot1d_outputs/`) as `--save_path`, not individual filenames.
- SPOT-1D automatically names each `.csv` file after the protein ID.

### Batch Prediction Command:

```bash
python code/run_spot1d_batch.py
```

The batch script picks each `.fasta` file from `data/fasta_files/`, runs SPOT-1D prediction, and saves the corresponding `.csv` output in `spot1d_outputs/`.

---

## Step 6: Structural Feature Extraction

Following the generation of SPOT-1D outputs, the following structural features were extracted:

| Feature Set                    | Number of Features |
|:--------------------------------|:------------------:|
| ASA Bigram                      | 1 |
| SS3 Autocovariance (Lag 10)      | 30 |
| Torsion Composition (Phi, Psi, Theta, Tau) | 4 |

Scripts used:

- `code/extract_asa_bigram.py` → outputs `features/asa_bigram.csv`
- `code/extract_ss3_autocov.py` → outputs `features/ss3_autocov.csv`
- `code/extract_torsion_composition.py` → outputs `features/torsion_composition.csv`

### Details:
- **ASA Bigram**: Mean of ASA[i] × ASA[i+2] across sequence.
- **SS3 Autocovariance**: Measures autocorrelation for Coil (C), Helix (H), and Strand (E) probabilities across 10 lags.
- **Torsion Composition**: Simple mean of torsion angles Phi, Psi, Theta, Tau.

---

## Final Folder Structure After Feature Extraction

```
ML_Final_project/
|
├── data/
│   └── fasta_files/          # All input .fasta files
├── pssm_outputs/              # PSI-BLAST output .pssm files
├── spot1d_outputs/            # SPOT-1D-Single output .csv files
├── features/                  # Extracted feature CSVs
│    ├── pssm_aao.csv
│    ├── pssm_sac.csv
│    ├── pssm_sd.csv
│    ├── asa_bigram.csv
│    ├── ss3_autocov.csv
│    └── torsion_composition.csv
├── code/
│    ├── run_psiblast.sh
│    ├── run_spot1d_batch.py
│    ├── extract_pssm_aao.py
│    ├── extract_pssm_sd.py
│    ├── extract_pssm_sac.py
│    ├── extract_asa_bigram.py
│    ├── extract_ss3_autocov.py
│    └── extract_torsion_composition.py
├── SPOT-1D-Single/             # SPOT-1D model code and models
├── README.md
├── environment.yml
└── requirements.txt
```

---

## Key Implementation Details and Fixes

- Replaced invalid amino acid 'U' with 'X' early to prevent PSI-BLAST and SPOT-1D failures.
- Standardized `.fasta` file generation.
- Corrected file path handling inside SPOT-1D-Single.
- Created clean, parallelized batch processing.
- Safely handled missing output files and sequences during feature extraction.

---



