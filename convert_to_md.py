#!/usr/bin/env python3
"""
convert_to_md.py — Convert PDF / Images → Markdown for LLM upload
Saves tokens by stripping noise and compressing whitespace.

Dependencies:
    pip install pymupdf pillow pytesseract
    # Also install Tesseract OCR engine:
    # Ubuntu/Debian: sudo apt install tesseract-ocr
    # macOS:         brew install tesseract
    # Windows:       https://github.com/UB-Mannheim/tesseract/wiki

Usage:
    python convert_to_md.py file1.pdf image.png file2.pdf photo.jpg
    python convert_to_md.py *.pdf *.png          # glob patterns
    python convert_to_md.py report.pdf            # single file
"""

import sys
import re
import argparse
from pathlib import Path


# ─── Helpers ─────────────────────────────────────────────────────────────────

def clean_text(text: str) -> str:
    """Remove noise that wastes tokens."""
    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Collapse 3+ blank lines → 2
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Strip trailing whitespace per line
    text = "\n".join(line.rstrip() for line in text.splitlines())
    # Remove common PDF header/footer junk (page numbers, URLs repeated every page)
    text = re.sub(r"(?m)^\s*\d+\s*$", "", text)          # lone page numbers
    text = re.sub(r"(?m)^\s*Page \d+ of \d+\s*$", "", text)  # "Page X of Y"
    # Final strip
    return text.strip()


def save_md(content: str, source_path: Path, output_dir: Path) -> Path:
    out_path = output_dir / (source_path.stem + ".md")
    out_path.write_text(content, encoding="utf-8")
    return out_path


# ─── PDF Converter ───────────────────────────────────────────────────────────

def pdf_to_md(pdf_path: Path) -> str:
    """
    Extract text from PDF using PyMuPDF.
    Falls back to OCR for scanned/image-only PDFs.
    """
    try:
        import fitz  # pymupdf
    except ImportError:
        sys.exit("❌ pymupdf not installed. Run: pip install pymupdf")

    doc = fitz.open(str(pdf_path))
    total_pages = len(doc)
    lines = [f"# {pdf_path.stem}", f"*Source: {pdf_path.name} — {total_pages} pages*\n"]

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text("text")  # plain text, preserves layout

        # Detect image-only page (no extractable text)
        if not text.strip():
            text = _ocr_page(page, page_num)

        if text.strip():
            lines.append(f"\n---\n## Page {page_num}\n")
            lines.append(clean_text(text))

    doc.close()
    return "\n".join(lines)


def _ocr_page(page, page_num: int) -> str:
    """OCR fallback for scanned PDF pages."""
    try:
        import pytesseract
        from PIL import Image
        import io
    except ImportError:
        print(f"  ⚠️  Page {page_num} is image-only. Install pytesseract+pillow for OCR.")
        return ""

    pix = page.get_pixmap(dpi=200)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    return pytesseract.image_to_string(img)


# ─── Image Converter ─────────────────────────────────────────────────────────

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif", ".webp", ".gif"}

def image_to_md(img_path: Path) -> str:
    """OCR an image file and return Markdown."""
    try:
        import pytesseract
        from PIL import Image
    except ImportError:
        sys.exit("❌ pillow/pytesseract not installed. Run: pip install pillow pytesseract")

    img = Image.open(str(img_path))

    # Preprocess: convert to greyscale for better OCR accuracy
    img = img.convert("L")

    text = pytesseract.image_to_string(img)
    lines = [
        f"# {img_path.stem}",
        f"*Source: {img_path.name}*\n",
        clean_text(text),
    ]
    return "\n".join(lines)


# ─── Main ────────────────────────────────────────────────────────────────────

def convert(file_path: Path, output_dir: Path) -> None:
    ext = file_path.suffix.lower()
    print(f"  Converting: {file_path.name}", end=" ... ")

    if ext == ".pdf":
        content = pdf_to_md(file_path)
    elif ext in IMAGE_EXTS:
        content = image_to_md(file_path)
    else:
        print(f"⚠️  Skipped (unsupported type: {ext})")
        return

    out = save_md(content, file_path, output_dir)
    size_kb = out.stat().st_size / 1024
    print(f"✅ → {out.name} ({size_kb:.1f} KB)")


def main():
    parser = argparse.ArgumentParser(
        description="Convert PDF/images to clean Markdown for LLM upload."
    )
    parser.add_argument("files", nargs="+", help="PDF or image file(s) to convert")
    parser.add_argument(
        "-o", "--output",
        default=".",
        help="Output directory (default: current directory)",
    )
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    files = [Path(f) for f in args.files]
    missing = [f for f in files if not f.exists()]
    if missing:
        print(f"❌ File(s) not found: {', '.join(str(f) for f in missing)}")
        sys.exit(1)

    print(f"\n📂 Output → {output_dir.resolve()}\n")
    for f in files:
        convert(f, output_dir)

    print("\nDone.")


if __name__ == "__main__":
    main()
