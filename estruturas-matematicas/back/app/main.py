from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import cv2
import base64
import numpy as np

app = Flask(__name__)
CORS(app)  # Adiciona suporte para CORS


def to_monochrome(image):
    for y in range(0, image.shape[0]):
      for x in range(0, image.shape[1]):

        (azul,verde,vermelho) = image[y,x]
        image[y,x] = (azul*0.114+verde*0.587+vermelho*0.299)

    return image.astype(np.uint8)

def to_blue(image):
    for y in range(0, image.shape[0]):
      for x in range(0, image.shape[1]):

        (azul,verde,vermelho) = image[y,x]
        image[y,x] = (azul,0,0)

    return image.astype(np.uint8)

def to_green(image):
    for y in range(0, image.shape[0]):
      for x in range(0, image.shape[1]):

        (azul,verde,vermelho) = image[y,x]
        image[y,x] = (0,verde,0)

    return image.astype(np.uint8)

def to_red(image):
    for y in range(0, image.shape[0]):
      for x in range(0, image.shape[1]):

        (azul,verde,vermelho) = image[y,x]
        image[y,x] = (0,0,vermelho)

    return image.astype(np.uint8)

def to_sepia(image):
    for y in range(0, image.shape[0]):
      for x in range(0, image.shape[1]):

        (azul,verde,vermelho) = image[y,x]
        tr = int(0.393 * vermelho + 0.769 * verde + 0.189 * azul)
        tg = int(0.349 * vermelho + 0.686 * verde + 0.168 * azul)
        tb = int(0.272 * vermelho + 0.534 * verde + 0.131 * azul)

        if tr > 255:
            tr = 255

        if tg > 255:
            tg = 255

        if tb > 255:
            tb = 255
        image[y,x] = (tb,tg,tr)

    return image.astype(np.uint8)

def to_negative(image):
    for y in range(0, image.shape[0]):
      for x in range(0, image.shape[1]):

        (azul,verde,vermelho) = image[y,x]
        tr = int(255 - vermelho)
        tg = int(255 - verde)
        tb = int(255 - azul)

        image[y,x] = (tb,tg,tr)
    return image.astype(np.uint8)

@app.route('/monochrome', methods=['POST'])
def monochrome():
    # pega a ibagem do request
    data = request.json

    if data:
        # tira do base64 e coloca em ibagem
        decoded_data = base64.b64decode(data['image_data'])
        # converte po numpy array
        image_array = cv2.imdecode(np.frombuffer(decoded_data, np.uint8), cv2.IMREAD_COLOR)
        # converte para monocromatica
        monochrome_image = to_monochrome(image_array)
        # codifica p base64 denovo
        _, encoded_monochrome = cv2.imencode('.png', monochrome_image)

        monochrome_data = base64.b64encode(encoded_monochrome).decode('utf-8')

        # devolve a responde
        return jsonify({'monochrome_data': monochrome_data})
    else:
        # se bichar ent quebra
        return jsonify({'error': 'No image data provided'}), 400

@app.route('/sepia', methods=['POST'])
def sepia():
    # pega a ibagem do request
    data = request.json

    if data:
        # tira do base64 e coloca em ibagem
        decoded_data = base64.b64decode(data['image_data'])
        # converte po numpy array
        image_array = cv2.imdecode(np.frombuffer(decoded_data, np.uint8), cv2.IMREAD_COLOR)
        # converte para monocromatica
        sepia_image = to_sepia(image_array)
        # codifica p base64 denovo
        _, encoded_sepia = cv2.imencode('.png', sepia_image)

        sepia_data = base64.b64encode(encoded_sepia).decode('utf-8')

        # devolve a responde
        return jsonify({'sepia_data': sepia_data})
    else:
        # se bichar ent quebra
        return jsonify({'error': 'No image data provided'}), 400
    
@app.route('/negative', methods=['POST'])
def negative():
    # pega a ibagem do request
    data = request.json

    if data:
        # tira do base64 e coloca em ibagem
        decoded_data = base64.b64decode(data['image_data'])
        # converte po numpy array
        image_array = cv2.imdecode(np.frombuffer(decoded_data, np.uint8), cv2.IMREAD_COLOR)
        # converte para monocromatica
        negative_image = to_negative(image_array)
        # codifica p base64 denovo
        _, encoded_negative = cv2.imencode('.png', negative_image)

        negative_data = base64.b64encode(encoded_negative).decode('utf-8')

        # devolve a responde
        return jsonify({'negative_data': negative_data})
    else:
        # se bichar ent quebra
        return jsonify({'error': 'No image data provided'}), 400
    
@app.route('/blue', methods=['POST'])
def blue():
    # pega a ibagem do request
    data = request.json

    if data:
        # tira do base64 e coloca em ibagem
        decoded_data = base64.b64decode(data['image_data'])
        # converte po numpy array
        image_array = cv2.imdecode(np.frombuffer(decoded_data, np.uint8), cv2.IMREAD_COLOR)
        # converte para monocromatica
        blue_image = to_blue(image_array)
        # codifica p base64 denovo
        _, encoded_blue = cv2.imencode('.png', blue_image)

        blue_data = base64.b64encode(encoded_blue).decode('utf-8')

        # devolve a responde
        return jsonify({'blue_data': blue_data})
    else:
        # se bichar ent quebra
        return jsonify({'error': 'No image data provided'}), 400

@app.route('/red', methods=['POST'])
def red():
    # pega a ibagem do request
    data = request.json

    if data:
        # tira do base64 e coloca em ibagem
        decoded_data = base64.b64decode(data['image_data'])
        # converte po numpy array
        image_array = cv2.imdecode(np.frombuffer(decoded_data, np.uint8), cv2.IMREAD_COLOR)
        # converte para monocromatica
        red_image = to_red(image_array)
        # codifica p base64 denovo
        _, encoded_red = cv2.imencode('.png', red_image)

        red_data = base64.b64encode(encoded_red).decode('utf-8')

        # devolve a responde
        return jsonify({'red_data': red_data})
    else:
        # se bichar ent quebra
        return jsonify({'error': 'No image data provided'}), 400

@app.route('/green', methods=['POST'])
def green():
    # pega a ibagem do request
    data = request.json

    if data:
        # tira do base64 e coloca em ibagem
        decoded_data = base64.b64decode(data['image_data'])
        # converte po numpy array
        image_array = cv2.imdecode(np.frombuffer(decoded_data, np.uint8), cv2.IMREAD_COLOR)
        # converte para monocromatica
        green_image = to_green(image_array)
        # codifica p base64 denovo
        _, encoded_green = cv2.imencode('.png', green_image)

        green_data = base64.b64encode(encoded_green).decode('utf-8')

        # devolve a responde
        return jsonify({'green_data': green_data})
    else:
        # se bichar ent quebra
        return jsonify({'error': 'No image data provided'}), 400
        
if __name__ == '__main__':
    app.run(debug=True)
