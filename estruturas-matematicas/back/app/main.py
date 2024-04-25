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
    for y in range(0, image.shape[0]):
        for x in range(0, image.shape[1]):
            (azul, verde, vermelho) = image[y, x]
            image[y, x] = (azul * 0.114 + verde * 0.587 + vermelho * 0.299)
    gray_image = image
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
            # Salva a imagem monocromática com nome diferente
            monochrome_filename = f"mono_{filename}"
            monochrome_path = os.path.join(app.config['UPLOAD_FOLDER'], monochrome_filename)
            cv2.imwrite(monochrome_path, monochrome_image)
            cv2.imshow('teste', monochrome_image)
            # Redireciona e passa o nome do arquivo monocromático
            return redirect(url_for('index', monochrome_image=monochrome_filename))

if __name__ == '__main__':
    app.run(debug=True)
