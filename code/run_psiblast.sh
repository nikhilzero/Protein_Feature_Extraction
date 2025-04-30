#!/bin/bash

INPUT_FOLDER="data/fasta_files"
OUTPUT_FOLDER="pssm_outputs"
DB="blast_db/uniprot_sprot.fasta"

mkdir -p $OUTPUT_FOLDER

NPROC=10  # Number of parallel jobs

count=0

for fasta in $INPUT_FOLDER/*.fasta
do
    filename=$(basename "$fasta" .fasta)

    # Launch psiblast in background
    psiblast -query "$fasta" -db "$DB" -num_iterations 3 -out_ascii_pssm "$OUTPUT_FOLDER/$filename.pssm" -evalue 0.001 &

    ((count++))

    # If count reaches NPROC, wait for all jobs to finish
    if [[ $count -ge $NPROC ]]
    then
        wait
        count=0
    fi
done

# Wait for any remaining jobs
wait
