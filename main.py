import io
from flask import Flask, request, jsonify, abort
import pdfplumber

app = Flask(__name__)

def extract_text_from_bytes(pdf_bytes: bytes) -> str:
    """
    Extrae texto de un PDF en memoria (bytes) usando pdfplumber.
    """
    text_content = ""
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text_content += page_text + "\n"
    return text_content

@app.route("/")
def index():
    return """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>PDF Text Extractor</title>
  <style>
    body { font-family: sans-serif; max-width: 600px; margin: 40px auto; }
    h1 { text-align: center; }
    form { display: flex; flex-direction: column; gap: 10px; }
    button { width: 120px; margin-top: 10px; }
    pre { white-space: pre-wrap; border: 1px solid #ccc; padding: 10px; margin-top: 20px; height: 300px; overflow: auto; }
  </style>
</head>
<body>
  <h1>PDF Text Extractor</h1>
  <p>Selecciona un PDF y pulsa “Extraer texto” para ver el contenido.</p>
  <form id="upload-form" enctype="multipart/form-data">
    <input type="file" id="file-input" name="file" accept="application/pdf" required>
    <button type="submit">Extraer texto</button>
  </form>
  <pre id="result"></pre>
  <script>
    document.getElementById('upload-form').addEventListener('submit', async function(e) {
      e.preventDefault();
      const input = document.getElementById('file-input');
      if (!input.files.length) return;
      const formData = new FormData();
      formData.append('file', input.files[0]);
      document.getElementById('result').textContent = 'Procesando…';
      try {
        const resp = await fetch('/extract', { method: 'POST', body: formData });
        if (!resp.ok) throw new Error('Error en servidor');
        const data = await resp.json();
        document.getElementById('result').textContent = data.text || '';
      } catch (err) {
        document.getElementById('result').textContent = 'Error: ' + err.message;
      }
    });
  </script>
</body>
</html>"""

@app.route("/extract", methods=["POST"])
def extract():
    """
    Handler HTTP: espera un form-data con key="file" y valor=archivo PDF.
    Retorna JSON { "text": "...texto extraído..." }.
    """
    if "file" not in request.files:
        return abort(400, "No se recibió ningún archivo bajo la clave 'file'.")

    archivo = request.files["file"]
    if not archivo.filename.lower().endswith(".pdf"):
        return abort(400, "Sólo se aceptan archivos .pdf")

    pdf_bytes = archivo.read()
    try:
        texto = extract_text_from_bytes(pdf_bytes)
    except Exception as e:
        return abort(500, f"Error extrayendo texto: {e}")

    return jsonify({"text": texto})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)