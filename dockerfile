FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir pymupdf

COPY extract_outline.py /app/extract_outline.py
COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
