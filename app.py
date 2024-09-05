from flask import Flask, render_template, request, send_file
import fitz
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads/'
COMPRESSED_FOLDER = 'compressed/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['COMPRESSED_FOLDER'] = COMPRESSED_FOLDER

def compress_pdf(input_pdf, output_pdf):
    try:
        doc = fitz.open(input_pdf)
        
        doc.save(output_pdf, garbage=4, deflate=True, clean=True)
        doc.close()

    except Exception as e:
        print(f"Erro ao comprimir o PDF: {e}")

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['pdf']
        prefix = request.form['prefix']

        if file:
            original_filename = file.filename.lower().replace(" ", "-")
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], prefix + original_filename)

            file.save(file_path)

            compressed_filename = f"{prefix}{original_filename}"
            compressed_file_path = os.path.join(app.config['COMPRESSED_FOLDER'], compressed_filename)
            compress_pdf(file_path, compressed_file_path)

            if not os.path.exists(compressed_file_path):
                return "Erro: O arquivo comprimido não foi encontrado.", 500

            return send_file(compressed_file_path, as_attachment=True)
    return render_template('index.html')

if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['COMPRESSED_FOLDER'], exist_ok=True)
    app.run(debug=True)
