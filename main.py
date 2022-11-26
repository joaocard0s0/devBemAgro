from flask import Flask, render_template, flash, request, redirect, send_file
from werkzeug.utils import secure_filename
import os
from conversaoArquivos import entrada_arquivo, limparArquivos


app = Flask(__name__)


UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)),'static\\files')

app.secret_key = "123"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['shp', 'dbf', 'shx', 'prj', 'cpg', 'kml','geojson'])


def allowed_file(filename):
 return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 

@app.route('/')
def upload_form():
  limparArquivos(UPLOAD_FOLDER)
  return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_file():
 if request.method == 'POST':
  if 'files[]' not in request.files:
   flash('No file part')
   return redirect(request.url)
  files = request.files.getlist('files[]')
  for file in files:
   if file and allowed_file(file.filename):
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
  flash('File(s) successfully uploaded')
  return redirect('/convert')


@app.route('/convert')
def convert():
  entrada_arquivo(UPLOAD_FOLDER)
  return render_template('dowload.html')
  

@app.route('/dowload')
def dowload_file():
  arquivo_zipado = r'{}\\lines.shp.zip'.format(UPLOAD_FOLDER)
  return send_file(arquivo_zipado, as_attachment=True)



if __name__ == '__main__':
 app.run(debug=True)