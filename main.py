#!/usr/bin/env python3
"""
Universal File Converter Application
A Flask-based web application for converting files between different formats
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import csv
import json
import html as html_module
import tempfile
from werkzeug.utils import secure_filename

app = Flask(__name__, 
            template_folder='public', 
            static_folder='src')

# Configuration
DOWNLOADS_FOLDER = os.path.expanduser('~/Downloads/FileConverter')
UPLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt', 'png', 'jpg', 'jpeg', 'xlsx', 'csv', 'pptx', 'webp', 'html', 'json'}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOADS_FOLDER'] = DOWNLOADS_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_file_extension(filename):
    """Get file extension"""
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else None


@app.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html')


@app.route('/api/convert', methods=['POST'])
def convert_file():
    """Handle file conversion"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'File type not allowed'}), 400

        to_format = request.form.get('to_format', '').lower()
        if not to_format:
            return jsonify({'success': False, 'error': 'Target format not specified'}), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        output_filename, output_path = convert_file_internal(filepath, to_format)

        if output_path and os.path.exists(output_path):
            return send_file(output_path, as_attachment=True, download_name=output_filename, mimetype='application/octet-stream')
        else:
            return jsonify({'success': False, 'error': 'Conversion failed'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


def convert_file_internal(filepath, target_format):
    """Internal file conversion logic - supports ALL required conversions"""
    source_format = get_file_extension(filepath)
    filename = os.path.basename(filepath)
    basename = filename.rsplit('.', 1)[0]
    output_filename = f"{basename}.{target_format}"
    output_path = os.path.join(app.config['DOWNLOADS_FOLDER'], output_filename)

    try:
        # ===== PDF as TARGET =====
        if target_format == 'pdf':
            if source_format == 'txt':
                pdf_from_text(filepath, output_path)
            elif source_format in ['docx', 'doc']:
                pdf_from_docx(filepath, output_path)
            elif source_format in ['png', 'jpg', 'jpeg']:
                pdf_from_image(filepath, output_path)
            elif source_format == 'xlsx':
                pdf_from_xlsx(filepath, output_path)
            elif source_format == 'csv':
                pdf_from_csv(filepath, output_path)
            elif source_format == 'pptx':
                pdf_from_pptx(filepath, output_path)
            else:
                raise ValueError(f"Cannot convert {source_format} to PDF")

        # ===== DOCX as TARGET =====
        elif target_format == 'docx':
            if source_format == 'txt':
                docx_from_text(filepath, output_path)
            elif source_format == 'pdf':
                docx_from_pdf(filepath, output_path)
            elif source_format == 'doc':
                doc_docx_copy(filepath, output_path)
            else:
                raise ValueError(f"Cannot convert {source_format} to DOCX")

        # ===== DOC as TARGET =====
        elif target_format == 'doc':
            if source_format == 'txt':
                docx_from_text(filepath, output_path)
            elif source_format == 'pdf':
                docx_from_pdf(filepath, output_path)
            elif source_format == 'docx':
                doc_docx_copy(filepath, output_path)
            else:
                raise ValueError(f"Cannot convert {source_format} to DOC")

        # ===== TXT as TARGET =====
        elif target_format == 'txt':
            if source_format == 'pdf':
                text_from_pdf(filepath, output_path)
            elif source_format in ['docx', 'doc']:
                text_from_docx(filepath, output_path)
            elif source_format == 'xlsx':
                text_from_xlsx(filepath, output_path)
            elif source_format == 'csv':
                text_from_csv(filepath, output_path)
            elif source_format == 'pptx':
                text_from_pptx(filepath, output_path)
            else:
                raise ValueError(f"Cannot convert {source_format} to TXT")

        # ===== HTML as TARGET =====
        elif target_format == 'html':
            if source_format == 'txt':
                html_from_text(filepath, output_path)
            else:
                raise ValueError(f"Cannot convert {source_format} to HTML")

        # ===== IMAGE as TARGET (PNG/JPG/JPEG) =====
        elif target_format in ['png', 'jpg', 'jpeg']:
            if source_format in ['png', 'jpg', 'jpeg', 'webp']:
                convert_image(filepath, output_path, target_format)
            elif source_format == 'pdf':
                image_from_pdf(filepath, output_path, target_format)
            elif source_format == 'pptx':
                image_from_pptx(filepath, output_path, target_format)
            else:
                raise ValueError(f"Cannot convert {source_format} to {target_format}")

        # ===== WEBP as TARGET =====
        elif target_format == 'webp':
            if source_format in ['png', 'jpg', 'jpeg']:
                convert_image(filepath, output_path, 'webp')
            else:
                raise ValueError(f"Cannot convert {source_format} to WEBP")

        # ===== XLSX as TARGET =====
        elif target_format == 'xlsx':
            if source_format == 'csv':
                xlsx_from_csv(filepath, output_path)
            else:
                raise ValueError(f"Cannot convert {source_format} to XLSX")

        # ===== CSV as TARGET =====
        elif target_format == 'csv':
            if source_format == 'xlsx':
                csv_from_xlsx(filepath, output_path)
            else:
                raise ValueError(f"Cannot convert {source_format} to CSV")

        # ===== JSON as TARGET =====
        elif target_format == 'json':
            if source_format == 'csv':
                json_from_csv(filepath, output_path)
            else:
                raise ValueError(f"Cannot convert {source_format} to JSON")

        else:
            raise ValueError(f"Conversion to {target_format} not supported")

        return output_filename, output_path
    except Exception as e:
        print(f"Conversion error: {str(e)}")
        raise


# ============================================================
# TEXT / HTML CONVERSIONS
# ============================================================
def pdf_from_text(input_path, output_path):
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    with open(input_path, 'r', errors='replace') as f:
        text = f.read()
    c = canvas.Canvas(output_path, pagesize=letter)
    y = 750
    for line in text.split('\n'):
        if y < 50:
            c.showPage()
            y = 750
        c.drawString(50, y, line[:100])
        y -= 15
    c.save()


def html_from_text(input_path, output_path):
    with open(input_path, 'r', errors='replace') as f:
        text = f.read()
    escaped = html_module.escape(text)
    lines = escaped.split('\n')
    body = '\n'.join(f'<p>{line}</p>' if line.strip() else '<br>' for line in lines)
    content = f'<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Document</title></head><body>{body}</body></html>'
    with open(output_path, 'w') as f:
        f.write(content)


# ============================================================
# DOCX/DOC CONVERSIONS
# ============================================================
def pdf_from_docx(input_path, output_path):
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from docx import Document
    doc = Document(input_path)
    text = '\n'.join([p.text for p in doc.paragraphs])
    c = canvas.Canvas(output_path, pagesize=letter)
    y = 750
    for line in text.split('\n'):
        if y < 50:
            c.showPage()
            y = 750
        c.drawString(50, y, line[:100])
        y -= 15
    c.save()


def docx_from_text(input_path, output_path):
    from docx import Document
    doc = Document()
    with open(input_path, 'r', errors='replace') as f:
        for line in f:
            doc.add_paragraph(line.strip())
    doc.save(output_path)


def docx_from_pdf(input_path, output_path):
    from docx import Document
    from PyPDF2 import PdfReader
    reader = PdfReader(input_path)
    doc = Document()
    for page in reader.pages:
        page_text = page.extract_text() or ''
        for line in page_text.split('\n'):
            if line.strip():
                doc.add_paragraph(line.strip())
    doc.save(output_path)


def doc_docx_copy(input_path, output_path):
    """Convert between DOC and DOCX (python-docx handles both as docx internally)"""
    from docx import Document
    doc = Document(input_path)
    doc.save(output_path)


def text_from_pdf(input_path, output_path):
    from PyPDF2 import PdfReader
    reader = PdfReader(input_path)
    text = '\n'.join([page.extract_text() or '' for page in reader.pages])
    with open(output_path, 'w') as f:
        f.write(text)


def text_from_docx(input_path, output_path):
    from docx import Document
    doc = Document(input_path)
    text = '\n'.join([p.text for p in doc.paragraphs])
    with open(output_path, 'w') as f:
        f.write(text)


# ============================================================
# IMAGE CONVERSIONS
# ============================================================
def pdf_from_image(input_path, output_path):
    from PIL import Image
    img = Image.open(input_path).convert('RGB')
    img.save(output_path)


def convert_image(input_path, output_path, format_type):
    from PIL import Image
    img = Image.open(input_path)
    if format_type == 'png':
        img = img.convert('RGBA')
        img.save(output_path, 'PNG')
    elif format_type in ['jpg', 'jpeg']:
        if img.mode in ('RGBA', 'LA', 'P'):
            bg = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'RGBA':
                bg.paste(img, mask=img.split()[-1])
            else:
                bg.paste(img)
            bg.save(output_path, 'JPEG', quality=95)
        else:
            img.convert('RGB').save(output_path, 'JPEG', quality=95)
    elif format_type == 'webp':
        img.save(output_path, 'WEBP', quality=90)


def image_from_pdf(input_path, output_path, format_type):
    try:
        from pdf2image import convert_from_path
        images = convert_from_path(input_path, dpi=150)
        if images:
            if format_type in ['jpg', 'jpeg']:
                images[0].save(output_path, 'JPEG', quality=95)
            else:
                images[0].save(output_path, 'PNG')
    except (ImportError, Exception):
        # Fallback: render text as image
        from PIL import Image, ImageDraw
        from PyPDF2 import PdfReader
        reader = PdfReader(input_path)
        text = '\n'.join([page.extract_text() or '' for page in reader.pages])
        lines = text.split('\n')
        w, lh = 800, 20
        h = max(400, len(lines) * lh + 80)
        img = Image.new('RGB', (w, h), 'white')
        draw = ImageDraw.Draw(img)
        y = 30
        for line in lines:
            if y > h - 30:
                break
            draw.text((30, y), line[:100], fill='black')
            y += lh
        if format_type in ['jpg', 'jpeg']:
            img.save(output_path, 'JPEG', quality=95)
        else:
            img.save(output_path, 'PNG')


# ============================================================
# SPREADSHEET CONVERSIONS
# ============================================================
def xlsx_from_csv(input_path, output_path):
    import openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    with open(input_path, 'r', newline='', errors='replace') as f:
        reader = csv.reader(f)
        for row in reader:
            ws.append(row)
    wb.save(output_path)


def csv_from_xlsx(input_path, output_path):
    import openpyxl
    wb = openpyxl.load_workbook(input_path)
    ws = wb.active
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        for row in ws.iter_rows(values_only=True):
            writer.writerow([str(c) if c is not None else '' for c in row])


def pdf_from_xlsx(input_path, output_path):
    import openpyxl
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    wb = openpyxl.load_workbook(input_path)
    ws = wb.active
    c = canvas.Canvas(output_path, pagesize=letter)
    y = 750
    for row in ws.iter_rows(values_only=True):
        if y < 50:
            c.showPage()
            y = 750
        line = '  |  '.join([str(cell) if cell is not None else '' for cell in row])
        c.drawString(50, y, line[:100])
        y -= 15
    c.save()


def text_from_xlsx(input_path, output_path):
    import openpyxl
    wb = openpyxl.load_workbook(input_path)
    ws = wb.active
    with open(output_path, 'w') as f:
        for row in ws.iter_rows(values_only=True):
            line = '\t'.join([str(c) if c is not None else '' for c in row])
            f.write(line + '\n')


def pdf_from_csv(input_path, output_path):
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(output_path, pagesize=letter)
    y = 750
    with open(input_path, 'r', errors='replace') as f:
        reader = csv.reader(f)
        for row in reader:
            if y < 50:
                c.showPage()
                y = 750
            c.drawString(50, y, '  |  '.join(row)[:100])
            y -= 15
    c.save()


def text_from_csv(input_path, output_path):
    with open(input_path, 'r', errors='replace') as f:
        content = f.read()
    lines = []
    reader = csv.reader(content.splitlines())
    for row in reader:
        lines.append('\t'.join(row))
    with open(output_path, 'w') as f:
        f.write('\n'.join(lines))


def json_from_csv(input_path, output_path):
    rows = []
    with open(input_path, 'r', newline='', errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(dict(row))
    with open(output_path, 'w') as f:
        json.dump(rows, f, indent=2)


# ============================================================
# PRESENTATION CONVERSIONS
# ============================================================
def pdf_from_pptx(input_path, output_path):
    from pptx import Presentation
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    prs = Presentation(input_path)
    c = canvas.Canvas(output_path, pagesize=letter)
    for i, slide in enumerate(prs.slides):
        if i > 0:
            c.showPage()
        y = 750
        c.drawString(50, y, f"--- Slide {i+1} ---")
        y -= 25
        for shape in slide.shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    t = para.text.strip()
                    if t:
                        if y < 50:
                            c.showPage()
                            y = 750
                        c.drawString(50, y, t[:100])
                        y -= 15
    c.save()


def text_from_pptx(input_path, output_path):
    from pptx import Presentation
    prs = Presentation(input_path)
    lines = []
    for i, slide in enumerate(prs.slides):
        lines.append(f"--- Slide {i+1} ---")
        for shape in slide.shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    t = para.text.strip()
                    if t:
                        lines.append(t)
        lines.append('')
    with open(output_path, 'w') as f:
        f.write('\n'.join(lines))


def image_from_pptx(input_path, output_path, format_type):
    from pptx import Presentation
    from PIL import Image, ImageDraw
    prs = Presentation(input_path)
    slide = prs.slides[0] if prs.slides else None
    if not slide:
        raise ValueError("No slides found")
    w, h = 800, 600
    img = Image.new('RGB', (w, h), 'white')
    draw = ImageDraw.Draw(img)
    y = 40
    for shape in slide.shapes:
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                t = para.text.strip()
                if t:
                    draw.text((40, y), t[:80], fill='black')
                    y += 25
    if format_type in ['jpg', 'jpeg']:
        img.save(output_path, 'JPEG', quality=95)
    else:
        img.save(output_path, 'PNG')


# ============================================================
# ERROR HANDLERS
# ============================================================
@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify({'success': False, 'error': 'File size exceeds 100MB limit'}), 413

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'success': False, 'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle server errors"""
    return jsonify({'success': False, 'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("🚀 File Converter App is starting...")
    print("📂 Upload folder: " + UPLOAD_FOLDER)
    print("📥 Downloads folder: " + DOWNLOADS_FOLDER)
    print("🌐 Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)
