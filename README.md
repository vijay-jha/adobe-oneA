# PDF Outline Extractor

## Approach
- Extracts PDF titles and headings using PyMuPDF.
- Outputs structured JSON format as per competition requirements.

## Libraries Used
- Python 3.10
- PyMuPDF

## How to Build & Run

### Build the Docker Image
```bash
docker build --platform linux/amd64 -t pdf-extractor .
```

### Run the Docker Image
```bash
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  pdf-extractor
```