from flask import Flask, request, render_template, send_file, redirect, url_for, flash, send_from_directory
import os, time, uuid

# Utilisation de pikepdf pour compresser les PDF
try:
    import pikepdf
except ImportError:
    pikepdf = None

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.secret_key = 'change-this-secret-in-production'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200 MB

def compress_pdf_pikepdf(input_path, output_path, compression_level='medium'):
    if pikepdf is None:
        raise RuntimeError('pikepdf is not installed. Install with: pip install pikepdf')
    pdf = pikepdf.open(input_path)
    pdf.save(output_path)
    pdf.close()
    return output_path

# Route principale
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Route de compression
@app.route('/compress', methods=['POST'])
def compress():
    file = request.files.get('file')
    level = request.form.get('level', 'medium')
    if not file:
        flash('No file uploaded', 'error')
        return redirect(url_for('index'))
    if not file.filename.lower().endswith('.pdf'):
        flash('Please upload a PDF file', 'error')
        return redirect(url_for('index'))

    uid = str(int(time.time())) + '_' + uuid.uuid4().hex[:8]
    in_path = os.path.join(app.config['UPLOAD_FOLDER'], uid + '_in.pdf')
    out_path = os.path.join(app.config['UPLOAD_FOLDER'], uid + '_out.pdf')
    file.save(in_path)
    try:
        compress_pdf_pikepdf(in_path, out_path, compression_level=level)
    except Exception as e:
        flash('Compression failed: ' + str(e), 'error')
        return redirect(url_for('index'))

    response = send_file(out_path, as_attachment=True, download_name=os.path.basename(out_path))

    # Nettoyage
    try:
        os.remove(in_path)
    except:
        pass
    try:
        os.remove(out_path)
    except:
        pass
    return response

# Route pour servir ads.txt pour AdSense
@app.route('/ads.txt')
def ads_txt():
    return send_from_directory('static', 'ads.txt')

# Lancement du serveur
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

