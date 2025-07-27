import fitz
import json
import argparse
import os

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    blocks = []

    for page_num, page in enumerate(doc, start=1):
        text_dict = page.get_text("dict")
        for block in text_dict["blocks"]:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span["text"].strip()
                    if not text or len(text) > 150:  # skip very long lines
                        continue
                    blocks.append({
                        "text": text,
                        "font_size": span["size"],
                        "is_bold": "Bold" in span["font"],
                        "page": page_num,
                        "y": line["bbox"][1]
                    })

    if not blocks:
        return {"title": os.path.splitext(os.path.basename(pdf_path))[0], "outline": []}

    # Sort blocks by page and position
    blocks.sort(key=lambda x: (x["page"], x["y"]))

    # Determine base font size
    font_sizes = sorted([b["font_size"] for b in blocks])
    body_size = font_sizes[len(font_sizes) // 2] if font_sizes else 12

    # Title = largest font on first page
    first_page_blocks = [b for b in blocks if b["page"] == 1]
    title_block = max(first_page_blocks, key=lambda x: x["font_size"], default=None)
    title = title_block["text"] if title_block else os.path.splitext(os.path.basename(pdf_path))[0]

    # Extract headings
    outline = []
    for b in blocks:
        if b["font_size"] >= body_size * 1.8:
            level = "H1"
        elif b["font_size"] >= body_size * 1.2:
            level = "H2"
        else:
            continue
        outline.append({"level": level, "text": b["text"], "page": b["page"]})

    return {"title": title, "outline": outline}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract headings from PDF into JSON")
    parser.add_argument("--pdf", required=True, help="Path to input PDF file")
    parser.add_argument("--output", help="Path to output JSON file")
    args = parser.parse_args()

    result = extract_outline(args.pdf)
    output_path = args.output if args.output else os.path.splitext(args.pdf)[0] + ".json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print(f"✅ Extracted outline saved to: {output_path}")
