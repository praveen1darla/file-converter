---
title: File Converter
emoji: 📄
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# ✨ Universal File Converter

A beautiful, modern web application that converts files between **34 different format combinations** — all running locally in your browser. Built with Flask (Python) backend and a glassmorphism-styled frontend.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.3-green?logo=flask&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Conversions](https://img.shields.io/badge/Conversions-34-purple)

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [How to Run](#-how-to-run)
- [API Reference](#-api-reference)
- [Supported Conversions (34)](#-supported-conversions--34-total)
- [Unsupported Conversions](#-unsupported-conversions)
- [Python Libraries Used](#-python-libraries-used)
- [Frontend Technologies](#-frontend-technologies)
- [Mobile Support](#-mobile-support)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)

---

## 🌟 Features

- **34 file conversions** across 10 file formats
- **Drag & drop** file upload
- **Auto-detection** of source format
- **Real-time progress bar** during conversion
- **Recent conversion history** stored in browser
- **Responsive design** — works on desktop, tablet & mobile
- **Animated gradient background** with glassmorphism UI
- **100MB max file size** support
- **No external APIs** — everything runs locally on your machine
- **Converted files saved** to `~/Downloads/FileConverter/`

---

## 🛠 Tech Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.10+ | Core programming language |
| **Flask** | 2.3.0 | Web framework (handles routes, API, file serving) |
| **Gunicorn** | Latest | Production WSGI server |

### Frontend
| Technology | Purpose |
|------------|---------|
| **HTML5** | Page structure & semantic markup |
| **Vanilla CSS** | Styling, animations, responsive design |
| **Vanilla JavaScript** | File handling, API calls, UI interactions |

### No External APIs
This app runs **100% locally**. No files are uploaded to any external server. All conversions happen on your machine using Python libraries.

---

## 📁 Project Structure

```
PDF_app/
├── main.py                    # 🐍 Flask backend — all conversion logic (535 lines)
├── wsgi.py                    # 🚀 WSGI entry point for production (Gunicorn)
├── requirements.txt           # 📦 Python dependencies
├── package.json               # 📋 Project metadata
│
├── public/                    # 🌐 Frontend HTML
│   └── index.html             # Main application page
│
├── src/                       # 🎨 Frontend assets
│   ├── components/
│   │   └── converter.js       # File upload, conversion logic, UI interactions
│   └── styles/
│       ├── main.css           # Core styles, layout, responsive design
│       ├── background.css     # Animated gradient background & blob effects
│       └── animations.css     # Keyframe animations & transitions
│
├── test_files/                # 🧪 Test files & automated test script
│   └── test_all_conversions.py
│
├── deploy.sh                  # 🚀 Production deployment script
├── setup.sh                   # ⚙️ Linux setup script
├── setup.bat                  # ⚙️ Windows setup script
├── file-converter.service     # 🔧 Systemd service for auto-start
├── nginx-config.conf          # 🌐 Nginx reverse proxy config
│
├── .venv/                     # Python virtual environment
└── venv/                      # Alternative virtual environment
```

---

## ⚙️ Installation & Setup

### Prerequisites
- **Python 3.10** or higher
- **pip** (Python package manager)

### Step 1: Clone / Navigate to project
```bash
cd /home/praveen/PDF_app
```

### Step 2: Create virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 (Optional): Install poppler for PDF→Image conversion
```bash
# Ubuntu / Debian
sudo apt-get install poppler-utils

# Fedora
sudo dnf install poppler-utils

# macOS
brew install poppler
```

> **Note:** Without poppler, PDF→PNG/JPG still works using a PIL text-rendering fallback.

---

## 🚀 How to Run

### Development Mode
```bash
source .venv/bin/activate
python main.py
```
Then open: **http://localhost:5000**

### Access from Mobile (same WiFi)
```bash
# Find your PC's IP address
hostname -I
# Example output: 10.216.66.11

# On mobile browser, go to:
# http://10.216.66.11:5000
```

### Production Mode (with Gunicorn)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

---

## 📡 API Reference

The app has **one API endpoint** for all conversions:

### `POST /api/convert`

Converts a file from one format to another.

**Request:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | File | ✅ Yes | The file to convert (max 100MB) |
| `to_format` | String | ✅ Yes | Target format (e.g., `pdf`, `docx`, `png`) |
| `from_format` | String | ❌ No | Source format (auto-detected if not provided) |

**Example with cURL:**
```bash
# Convert a TXT file to PDF
curl -X POST http://localhost:5000/api/convert \
  -F "file=@document.txt" \
  -F "to_format=pdf" \
  --output document.pdf

# Convert a PNG to WEBP
curl -X POST http://localhost:5000/api/convert \
  -F "file=@image.png" \
  -F "to_format=webp" \
  --output image.webp

# Convert CSV to JSON
curl -X POST http://localhost:5000/api/convert \
  -F "file=@data.csv" \
  -F "to_format=json" \
  --output data.json
```

**Success Response:** Returns the converted file as a download (binary)

**Error Response:**
```json
{
  "success": false,
  "error": "Cannot convert xlsx to pptx"
}
```

### `GET /`

Serves the main web application page.

---

## ✅ Supported Conversions — 34 Total

### 📄 From Text (.TXT) — 4 conversions
| To | Library Used |
|-----|-------------|
| PDF | ReportLab |
| DOCX | python-docx |
| DOC | python-docx |
| HTML | Built-in (html module) |

### 📕 From Word (.DOCX) — 3 conversions
| To | Library Used |
|-----|-------------|
| PDF | python-docx + ReportLab |
| TXT | python-docx |
| DOC | python-docx (copy) |

### 📕 From Word (.DOC) — 3 conversions
| To | Library Used |
|-----|-------------|
| PDF | python-docx + ReportLab |
| DOCX | python-docx (copy) |
| TXT | python-docx |

### 📕 From PDF (.PDF) — 5 conversions
| To | Library Used |
|-----|-------------|
| DOCX | PyPDF2 + python-docx |
| DOC | PyPDF2 + python-docx |
| TXT | PyPDF2 |
| PNG | pdf2image / Pillow fallback |
| JPG | pdf2image / Pillow fallback |

### 🖼️ From PNG (.PNG) — 3 conversions
| To | Library Used |
|-----|-------------|
| JPG | Pillow |
| PDF | Pillow |
| WEBP | Pillow |

### 🖼️ From JPG/JPEG (.JPG / .JPEG) — 5 conversions
| To | Library Used |
|-----|-------------|
| PNG | Pillow |
| PDF | Pillow |
| WEBP | Pillow |
| *(JPEG→PNG)* | Pillow |
| *(JPEG→JPG)* | Pillow |

### 📊 From Excel (.XLSX) — 3 conversions
| To | Library Used |
|-----|-------------|
| CSV | openpyxl |
| PDF | openpyxl + ReportLab |
| TXT | openpyxl |

### 📊 From CSV (.CSV) — 4 conversions
| To | Library Used |
|-----|-------------|
| XLSX | openpyxl |
| PDF | csv + ReportLab |
| TXT | csv module |
| JSON | csv + json module |

### 🎬 From PowerPoint (.PPTX) — 4 conversions
| To | Library Used |
|-----|-------------|
| PDF | python-pptx + ReportLab |
| PNG | python-pptx + Pillow |
| JPG | python-pptx + Pillow |
| TXT | python-pptx |

---

## 🚫 Unsupported Conversions

These conversions are **NOT possible** in this app:

| Conversion | Reason |
|-----------|--------|
| PDF → PPTX | Complex layout reconstruction |
| PDF → XLSX/CSV | No tabular structure in PDF |
| DOCX → XLSX | Incompatible data types |
| DOCX → PPTX | Complex conversion |
| Image → TXT | Would need OCR (Tesseract) |
| Image → DOCX | Not a document format |
| XLSX → DOCX | Incompatible data types |
| PPTX → DOCX | Complex layout conversion |
| Video/Audio | Requires ffmpeg (not installed) |
| ZIP/RAR | Archive tools not included |
| GIF → WEBP | Animation support needed |

---

## 📦 Python Libraries Used

| Library | Version | What It Does |
|---------|---------|-------------|
| **Flask** | 2.3.0 | Web framework — routes, API, file serving |
| **python-docx** | 0.8.11 | Read/write Microsoft Word (.docx) files |
| **PyPDF2** | 3.0.1 | Read PDF files, extract text from pages |
| **Pillow** | 9.5.0 | Image processing — convert PNG, JPG, WEBP |
| **python-pptx** | 0.6.21 | Read PowerPoint (.pptx) presentations |
| **pdf2image** | 1.16.3 | Convert PDF pages to images (needs poppler) |
| **ReportLab** | 4.0.4 | Generate PDF files from text/data |
| **openpyxl** | 3.1.2 | Read/write Excel (.xlsx) spreadsheets |
| **python-magic** | 0.4.27 | File type detection by content |

### How each library is used in conversions:

```
ReportLab ──────► Creates PDF from TXT, DOCX, CSV, XLSX, PPTX
python-docx ────► Reads/writes DOCX, converts TXT↔DOCX, PDF→DOCX
PyPDF2 ─────────► Reads PDF, extracts text for PDF→TXT, PDF→DOCX
Pillow ─────────► Converts images (PNG↔JPG↔WEBP↔PDF), renders fallbacks
python-pptx ────► Reads PPTX slides, extracts text and renders images
openpyxl ───────► Reads/writes XLSX, converts CSV↔XLSX
pdf2image ──────► Converts PDF pages to high-quality PNG/JPG images
```

---

## 🎨 Frontend Technologies

### HTML (`public/index.html`)
- Semantic HTML5 structure
- Drag & drop file upload area
- Format selection dropdowns (From/To)
- Progress bar and status messages
- Recent conversions list

### CSS (3 files in `src/styles/`)

| File | What It Does |
|------|-------------|
| **main.css** | Core layout, converter card, buttons, responsive breakpoints |
| **background.css** | Animated gradient background with 4 floating blob effects |
| **animations.css** | Keyframe animations for UI elements (slide, fade, pulse) |

**Design features:**
- Glassmorphism cards (`backdrop-filter: blur(20px)`)
- Animated gradient background (shifts through purple/pink/blue)
- 4 floating gradient blobs with independent animation cycles
- Responsive: stacks vertically on screens < 768px

### JavaScript (`src/components/converter.js`)
- `FileConverter` class handles all UI logic
- Drag & drop with visual feedback
- Auto-detects file format from extension
- Sends files to `/api/convert` via `fetch()` API
- Downloads converted file using Blob + URL.createObjectURL
- Stores recent conversions in `localStorage`

---

## 📱 Mobile Support

The app is fully responsive and works on mobile browsers:

| Feature | Desktop | Mobile |
|---------|---------|--------|
| File upload | Drag & drop + click | Click to select |
| Format dropdowns | Side by side | Stacked vertically |
| Convert button | Full width | Full width |
| Progress bar | ✅ | ✅ |
| Recent history | ✅ | ✅ |
| Download files | ✅ | ✅ (saves to Downloads) |

**Access on mobile:** Open `http://<your-pc-ip>:5000` on any device connected to the same WiFi.

---

## 🚀 Deployment

### Option 1: Systemd Service (Linux — runs 24/7)
```bash
sudo cp file-converter.service /etc/systemd/system/
sudo systemctl enable file-converter
sudo systemctl start file-converter
```

### Option 2: Nginx Reverse Proxy
```bash
sudo cp nginx-config.conf /etc/nginx/sites-available/file-converter
sudo ln -s /etc/nginx/sites-available/file-converter /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

### Option 3: Quick Deploy Script
```bash
bash deploy.sh
```

---

## 🔍 Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| Port 5000 already in use | Run `lsof -ti:5000 \| xargs kill -9` |
| PDF→PNG low quality | Install poppler: `sudo apt install poppler-utils` |
| XLSX conversions fail | Run `pip install openpyxl` |
| Can't access from mobile | Check firewall: `sudo ufw allow 5000` |
| File too large | Max size is 100MB, compress file first |

---

## 📊 Quick Stats

```
Total file formats supported:  10 (TXT, PDF, DOCX, DOC, PNG, JPG, WEBP, XLSX, CSV, PPTX, HTML, JSON)
Total conversions possible:    34
Total Python libraries:        9
Backend framework:             Flask 2.3
Frontend:                      Pure HTML + CSS + JavaScript (no frameworks)
Max file size:                 100 MB
External APIs used:            0 (fully offline)
Lines of Python code:          ~535
Lines of JavaScript:           ~316
Lines of CSS:                  ~570
```

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

**Made with ❤️ by Praveen**
