from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import cv2
import base64
import numpy as np

app = Flask(__name__)
CORS(app)  # Adiciona suporte para CORS


def to_monochrome(image):
    """Converts an image to monochrome (grayscale).

  Args:
      image: A NumPy array representing the image.

  Returns:
      A NumPy array representing the monochrome image.
  """
    # Convert BGR to grayscale using weighted sum
    gray = np.dot(image, [0.114, 0.587, 0.299])
    return gray.astype(np.uint8)  # Ensure byte data type


@app.route('/monochrome', methods=['POST'])
def monochrome():
    # Get image data from request
    data = request.json

    if data:
        # Decode base64 encoded image data
        decoded_data = base64.b64decode(data['image_data'])
        # Convert decoded data to NumPy array
        image_array = cv2.imdecode(np.frombuffer(decoded_data, np.uint8), cv2.IMREAD_COLOR)
        # Convert to monochrome
        monochrome_image = to_monochrome(image_array)
        # Encode monochrome image to base64 for response
        _, encoded_monochrome = cv2.imencode('.png', monochrome_image)

        monochrome_data = base64.b64encode(encoded_monochrome).decode('utf-8')
        return jsonify({'monochrome_data': monochrome_data})
    else:
        return jsonify({'error': 'No image data provided'}), 400


if __name__ == '__main__':
    app.run(debug=True)
