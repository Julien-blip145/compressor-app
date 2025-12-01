from flask import Flask, request, render_template, send_file, redirect, url_for, flash
import os, time, uuid, subprocess
from PIL import Image

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.secret_key = 'change-this-secret-in-production'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200 MB

# ----------------------------
# Fonction Ghostscript pour PDF
# ----------------------------
def compress_pdf(input_path, output_path):
    """
    Compression PDF forte (screen) garantie
    """
    cmd = [
        "gswin64c",
        "-sDEVICE=pdfwrite",
        f"-sOutputFile={output_path}",
        "-dPDFSETTINGS=/screen",
        "-dNOPAUSE",
        "-dBATCH",
        input_path
    ]
    subprocess.run(cmd, shell=True)
    return output_path

# ----------------------------
# Fonction compression images
# ----------------------------
def compress_image(input_path, output_path, quality=70):
    image = Image.open(input_path)
    image.save(output_path, optimize=True, quality=quality)
    return output_path

# ----------------------------
# Routes Flask
# ----------------------------
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress():
    file = request.files.get('file')
    level = request.form.get('level', 'medium')

    if not file:
        flash('No file uploaded', 'error')
        return redirect(url_for('index'))

    filename = file.filename
    ext = filename.split('.')[-1].lower()

    uid = str(int(time.time())) + '_' + uuid.uuid4().hex[:8]
    in_path = os.path.join(app.config['UPLOAD_FOLDER'], uid + '_in.' + ext)
    out_path = os.path.join(app.config['UPLOAD_FOLDER'], uid + '_out.' + ext)
    file.save(in_path)

    try:
        if ext == 'pdf':
            compress_pdf(in_path, out_path)
        elif ext in ['jpg', 'jpeg', 'png']:
            q_map = {'low': 90, 'medium': 70, 'high': 50}
            compress_image(in_path, out_path, q_map.get(level, 70))
        else:
            # Autres fichiers : renvoyer le fichier original
            out_path = in_path
    except Exception as e:
        flash('Compression failed: ' + str(e), 'error')
        return redirect(url_for('index'))

    # Taille avant/après compression
    size_before = os.path.getsize(in_path)
    size_after = os.path.getsize(out_path)

    # Envoyer le fichier compressé avec tailles dans les headers
    response = send_file(out_path, as_attachment=True, download_name=filename)
    response.headers['X-Size-Before'] = str(size_before)
    response.headers['X-Size-After'] = str(size_after)

    if out_path != in_path:
        try:
            os.remove(in_path)
            os.remove(out_path)
        except:
            pass

    return response

# ----------------------------
# Lancer l'application
# ----------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
