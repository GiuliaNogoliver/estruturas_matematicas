from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import cv2
import base64
import numpy as np
import math

app = Flask(__name__)
CORS(app)  # Adiciona suporte para CORS

def to_monochrome(rgb):

    r, g, b= rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]

    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray.astype(np.uint8)

def to_blue(rgb):

    r, g, b= rgb[:,:,0], rgb[:,:,1], rgb[:,:,2] 

    blue = np.dstack((b,g*0,r*0))

    return blue.astype(np.uint8)

def to_green(rgb):

    r, g, b= rgb[:,:,0], rgb[:,:,1], rgb[:,:,2] 

    green = np.dstack((b*0,g,r*0))

    return green.astype(np.uint8)

def to_red(rgb):

    r, g, b= rgb[:,:,0], rgb[:,:,1], rgb[:,:,2] 

    red = np.dstack((b*0,g*0,r))

    return red.astype(np.uint8)

def to_sepia(rgb):
    
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]

    tr = 0.393 * r + 0.769 * g + 0.189 * b
    tg = 0.349 * r + 0.686 * g + 0.168 * b
    tb = 0.272 * r + 0.534 * g + 0.131 * b

    tr[tr>255] = 255
    tg[tg>255] = 255
    tb[tb>255] = 255

    sepia = np.dstack((tb,tg,tr))

    return sepia.astype(np.uint8)

def to_negative(rgb):
    
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]

    tr = 255 - r
    tg = 255 - g
    tb = 255 - b

    negative = np.dstack((tr,tg,tb))

    return negative.astype(np.uint8)

def shear(angle,x,y):
    '''
    |1  -tan(𝜃/2) |  |1        0|  |1  -tan(𝜃/2) | 
    |0      1     |  |sin(𝜃)   1|  |0      1     |
    '''
    # shear 1
    tangent=math.tan(angle/2)
    new_x=round(x-y*tangent)
    new_y=y
    
    #shear 2
    new_y=round(new_x*math.sin(angle)+new_y)

    #shear 3
    new_x=round(new_x-new_y*tangent)
    
    return new_y,new_x


def to_changes(img,scale,bright,angle):

    image = np.array(img)

    
    angle=math.radians(int(angle))
    cosine=math.cos(angle)
    sine=math.sin(angle)

    height=image.shape[0]
    width=image.shape[1]

    new_height  = round(abs(image.shape[0]*cosine)+abs(image.shape[1]*sine))+1
    new_width  = round(abs(image.shape[1]*cosine)+abs(image.shape[0]*sine))+1

    output=np.zeros((new_height,new_width,image.shape[2]))
    image_copy=output.copy()

    original_centre_height   = round(((image.shape[0]+1)/2)-1)
    original_centre_width    = round(((image.shape[1]+1)/2)-1)

   
    new_centre_height= round(((new_height+1)/2)-1)
    new_centre_width= round(((new_width+1)/2)-1)  


    for i in range(height):
        for j in range(width):
            
            y=image.shape[0]-1-i-original_centre_height                   
            x=image.shape[1]-1-j-original_centre_width 

                             
            new_y,new_x=shear(angle,x,y)

            
            
            new_y=new_centre_height-new_y
            new_x=new_centre_width-new_x

            output[new_y,new_x,:]=image[i,j,:]

    r, g, b = output[:,:,0], output[:,:,1], output[:,:,2]

    bright = float(bright)

    tr = r * bright
    tg = g * bright
    tb = b * bright

    img2 = np.dstack((tr,tg,tb))


    return img2

@app.route('/apply', methods=['POST'])
def apply():
    # pega a ibagem do request
    data = request.json

    if data:
        # tira do base64 e coloca em ibagem
        decoded_data = base64.b64decode(data['image_data'])
        scale, brightness, rotation = data['scale_data'], data['brightness_data'], data['rotation_data']
        # converte po numpy array
        image_array = cv2.imdecode(np.frombuffer(decoded_data, np.uint8), cv2.IMREAD_COLOR)
        # converte para monocromatica
        monochrome_image = to_changes(image_array, scale, brightness, rotation)
        # codifica p base64 denovo
        _, encoded_monochrome = cv2.imencode('.png', monochrome_image)

        monochrome_data = base64.b64encode(encoded_monochrome).decode('utf-8')

        # devolve a responde
        return jsonify({'monochrome_data': monochrome_data})
    else:
        # se bichar ent quebra
        return jsonify({'error': 'No image data provided'}), 400

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
