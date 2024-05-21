from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import cv2
import base64
import numpy as np
import math
from itertools import chain

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

def set_scale(img,h,w):
    
    scale_h = h / img.shape[0]
    scale_w = w / img.shape[1]
 
    rows = np.arange(h)[:, np.newaxis] / scale_h
    cols = np.arange(w) / scale_w
    new_img = img[np.floor(rows).astype(int), np.floor(cols).astype(int)]
 
    return new_img.astype(np.uint8)

def shear(angle,x,y):

    tangent=math.tan(angle/2)
    new_x=np.round(x-y*tangent)
    new_y=y
    
    new_y=np.round(new_x*math.sin(angle)+new_y)

    new_x=np.round(new_x-new_y*tangent)        
    
    return new_y,new_x

def set_angle(img,angle):

    rot_rad = angle * np.pi / 180.0
    rotate_m = np.array([[np.cos(rot_rad), np.sin(rot_rad)],
                         [- np.sin(rot_rad), np.cos(rot_rad)]])

    gray_scale = False
    if len(img.shape) < 3:
        img = img.reshape(*img.shape, 1)
        gray_scale = True

    h, w, c = img.shape

    rotated_image = np.zeros((h, w, c))

    indices_org = np.array(np.meshgrid(np.arange(h), np.arange(w))).reshape(2, -1)
    indices_new = indices_org.copy()
    indices_new = np.dot(rotate_m, indices_new).astype(int)
    mu1 = np.mean(indices_new, axis=1).astype(int).reshape((-1, 1))
    mu2 = np.mean(indices_org, axis=1).astype(int).reshape((-1, 1))
    indices_new += (mu2-mu1)   

    t0, t1 = indices_new
    t0 = (0 <= t0) & (t0 < h)
    t1 = (0 <= t1) & (t1 < w)
    valid = t0 & t1
    indices_new = indices_new.T[valid].T
    indices_org = indices_org.T[valid].T

    #
    xind, yind = indices_new
    xi,yi=shear(angle,xind,yind)
    xi, yi = indices_org
    rotated_image[xi, yi, :] = img[xind, yind, :]

    if gray_scale:
        rotated_image = rotated_image.reshape((h, w))

    return rotated_image.astype(np.uint8)

def set_translation(img, dir,value):
    value = int(value)
    match dir:
        case 'left':
            img_2 = np.zeros_like(img)
            img_2[:,:-value] = img[:,value:]
        case 'up':
            img_2 = np.zeros_like(img)
            img_2[:-value,:] = img[value:,:]
        case 'down':
            img_2 = np.zeros_like(img)
            img_2[value:,:] = img[:-value,:]
        case 'right':
            img_2 = np.zeros_like(img)
            img_2[:,value:] = img[:,:-value]
        

    return img_2.astype(np.uint8)

def translation_right(img):

    img_2 = np.zeros_like(img)
    img_2[:,10:] = img[:,:-10]

def to_changes(img,scale,bright,angle):


    image = np.array(img)
    scale = float(scale)
    angle = float(angle)
    
    bright = float(bright)

    r, g, b = image[:,:,0], image[:,:,1], image[:,:,2]

    tr = r * bright
    tg = g * bright
    tb = b * bright

    tr[tr>255] = 255
    tg[tg>255] = 255
    tb[tb>255] = 255

    image_2 = np.dstack((tr,tg,tb))
    
    image_3 = set_angle(image_2,angle)

    height_3 = int(image.shape[0]*scale)
    width_3 = int(image.shape[1]*scale)

    img_final = set_scale(image_3,height_3,width_3)

    return img_final.astype(np.uint8)

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
        new_image = to_changes(image_array, scale, brightness, rotation)
        # codifica p base64 denovo
        _, encoded_new_image = cv2.imencode('.png', new_image)

        new_data = base64.b64encode(encoded_new_image).decode('utf-8')

        # devolve a responde
        return jsonify({'monochrome_data': new_data})
    else:
        # se bichar ent quebra
        return jsonify({'error': 'No image data provided'}), 400

@app.route('/translation', methods=['POST'])
def translation():
    # pega a ibagem do request
    data = request.json

    if data:
        # tira do base64 e coloca em ibagem
        decoded_data = base64.b64decode(data['image_data'])
        direction = data['direction']
        value = data['value_data']
        # converte po numpy array
        image_array = cv2.imdecode(np.frombuffer(decoded_data, np.uint8), cv2.IMREAD_COLOR)
        # converte para monocromatica
        trans_image = set_translation(image_array, direction,value)
        # codifica p base64 denovo
        _, encoded_trans_image = cv2.imencode('.png', trans_image)

        new_data = base64.b64encode(encoded_trans_image).decode('utf-8')

        # devolve a responde
        return jsonify({'trans_data': new_data})
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
