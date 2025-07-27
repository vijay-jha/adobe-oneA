#!/bin/sh
set -e

echo "Starting PDF Outline Extraction..."

# Process all PDFs in /app/input
for file in /app/input/*.pdf; do
    [ -e "$file" ] || continue
    filename=$(basename "$file" .pdf)
    echo "Processing $filename..."
    python3 /app/t5.py --pdf "$file" --output "/app/output/$filename.json"
done

echo "All files processed. Output saved to /app/output."
