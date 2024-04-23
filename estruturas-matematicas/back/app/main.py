# Arquivo principal da aplicação Flask
from flask import Flask, render_template, request, redirect, url_for
import cv2
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'


def to_monochrome(image_path):
    # Carrega a imagem
    image = cv2.imread(image_path)
    # Converte para escala de cinza
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image


@app.route('/')
def index():
    # Se o caminho da imagem monocromática foi passado como argumento
    monochrome_image = request.args.get('monochrome_image')
    return render_template('index.html', monochrome_image=monochrome_image)


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            # Converte a imagem para monocromático
            monochrome_image = to_monochrome(file_path)
            # Salva a imagem monocromática
            cv2.imwrite(file_path, monochrome_image)
            cv2.imshow('teste',monochrome_image)
            # Redireciona para a página inicial e passa o caminho do arquivo monocromático
            return redirect(url_for('index', monochrome_image=file_path))

if __name__ == '__main__':
    app.run(debug=True)
