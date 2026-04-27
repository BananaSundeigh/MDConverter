# 📄 MDConverter — PDF & Image to Markdown Converter
> v2.0.0

Convert PDFs and images into clean, token-efficient Markdown files — optimized for uploading to LLMs like Claude, ChatGPT, and Gemini.

---

## 🧠 Why Convert to Markdown Before Uploading?

When you upload a raw PDF or image to an LLM, you waste tokens on:
- Binary encoding overhead
- Embedded fonts, metadata, and formatting noise
- Repeated boilerplate (headers, footers, page numbers)
- Blank lines and trailing whitespace

By converting to `.md` first, you send **only the content that matters** — dramatically reducing token usage and cost.

| Format | Avg Token Usage | Notes |
|--------|----------------|-------|
| Raw PDF upload | ~3,000–8,000 tokens | Includes encoding overhead |
| Image upload | ~1,500–4,000 tokens | Vision model processing |
| Converted `.md` | ~500–2,000 tokens | Text only, noise removed |

> 💡 A 10-page document can go from **6,000 → 1,200 tokens** after conversion — an 80% reduction.

---

## ✨ Features

- ✅ **PDF → Markdown** — fast text extraction with PyMuPDF
- ✅ **Image → Markdown** — OCR via Tesseract (`.png`, `.jpg`, `.jpeg`, `.bmp`, `.tiff`, `.webp`, `.gif`)
- ✅ **Scanned PDF support** — auto-detects image-only pages and applies OCR fallback
- ✅ **Token-saving cleanup** — strips page numbers, collapses blank lines, removes trailing whitespace
- ✅ **Batch conversion** — convert multiple files in one command
- ✅ **Custom output directory** — organize all `.md` files in one place
- ✅ **Auto-generates CLI launcher** — creates `pdftomd.bat` automatically on first run if missing
- ✅ **Global CLI command** — run `pdftomd` from anywhere

---

## 🔧 How It Works

```
Input (PDF / Image)
        │
        ▼
┌───────────────────┐
│   File Type Check │
└───────┬───────────┘
        │
   ┌────┴────┐
   │         │
  PDF      Image
   │         │
   ▼         ▼
PyMuPDF   Tesseract OCR
extract   (pytesseract
text      + Pillow)
   │         │
   └────┬────┘
        ▼
┌───────────────────┐
│   Text Cleaner    │  ← strips noise, collapses whitespace,
│                   │    removes page numbers & boilerplate
└───────────────────┘
        │
        ▼
   Output .md file
```

**For scanned PDFs**, the script automatically detects pages with no extractable text and falls back to OCR — no manual intervention needed.

**On first run**, the script checks for `pdftomd.bat` and creates it automatically if missing — no manual setup required.

---

## 📦 Installation

**1. Clone the repo**
```bash
git clone https://github.com/BananaSundeigh/MDConverter.git
cd MDConverter
```

**2. Create a virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # macOS/Linux
```

**3. Install Python dependencies**
```bash
pip install pymupdf pillow pytesseract numpy
```

**4. Install Tesseract OCR engine**
- Windows: [UB-Mannheim installer](https://github.com/UB-Mannheim/tesseract/wiki)
- macOS: `brew install tesseract`
- Ubuntu: `sudo apt install tesseract-ocr`

**5. Add Tesseract to PATH** (Windows)
```powershell
[Environment]::SetEnvironmentVariable("Path", [Environment]::GetEnvironmentVariable("Path", "User") + ";C:\path\to\Tesseract-OCR", "User")
```

---

## 🚀 Usage

```bash
# Single PDF
python convert_to_md.py report.pdf

# Single image
python convert_to_md.py scan.png

# Multiple files
python convert_to_md.py file1.pdf image.jpg file2.pdf

# Custom output directory
python convert_to_md.py report.pdf -o ./output

# Windows global command (auto-created on first run)
pdftomd "C:\path\to\file.pdf"
pdftomd "C:\path\to\scan.png"
```

---

## 🗂 Output Example

Input: `lecture.pdf` (3 pages)

```markdown
# lecture
*Source: lecture.pdf — 3 pages*

---
## Page 1

Introduction to Algorithms
Lecture notes — Week 9
...

---
## Page 2

Floyd-Warshall Algorithm
...
```

---

## 🛠 Tech Stack

| Tool | Purpose |
|------|---------|
| [PyMuPDF](https://pymupdf.readthedocs.io/) | Fast PDF text extraction |
| [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) | Image & scanned PDF text recognition |
| [pytesseract](https://github.com/madmaze/pytesseract) | Python wrapper for Tesseract |
| [Pillow](https://python-pillow.org/) | Image preprocessing (grayscale for better OCR accuracy) |

---

## 📁 Project Structure

```
MDConverter/
├── convert_to_md.py   # Main conversion script
├── pdftomd.bat        # Windows global launcher (auto-generated)
├── output/            # Default output directory
├── README.md
└── .venv/             # Python virtual environment
```

---

## 📋 Supported File Types

| Type | Extensions |
|------|-----------|
| PDF | `.pdf` |
| Images | `.png`, `.jpg`, `.jpeg`, `.bmp`, `.tiff`, `.tif`, `.webp`, `.gif` |

---

## 📝 Changelog

### v2.0.0
- Auto-generates `pdftomd.bat` on first run if missing
- Paths resolved relative to script location (no hardcoded usernames)
- Output folder auto-created if it doesn't exist

### v1.0.0
- Initial release
- PDF and image to Markdown conversion
- Tesseract OCR fallback for scanned pages
- Token-saving text cleanup

---

## 📄 License

MIT
