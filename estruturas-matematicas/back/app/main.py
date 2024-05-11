from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import cv2
import base64
import numpy as np

app = Flask(__name__)
CORS(app)  # Adiciona suporte para CORS


def to_monochrome(image):
    gray = np.dot(image, [0.114, 0.587, 0.299])
    return gray.astype(np.uint8)


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


if __name__ == '__main__':
    app.run(debug=True)
