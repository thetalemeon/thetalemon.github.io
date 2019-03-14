from flask import Flask, render_template, jsonify, request
from random import *
import cv2
import string
import utils
import prosImage
import playSound
import base64
import struct
from scipy.io import wavfile

app = Flask(__name__,
                    static_folder = "./dist/static",
                                template_folder = "./dist")

@app.route("/api/testpost", methods=['POST'])
def hello():
    response = {
        "result": int(request.json["val1"].split()[0])*2
    }
    return jsonify(response)

@app.route('/api/random')
def random_number():
    response = {
        'randomNumber': randint(1, 100)
    }
    return jsonify(response)

@app.route('/api/cannyFile', methods=['POST'])
def upload():
    base64_png = request.form['image']
    img_array = utils.base64toCV2(base64_png)

    processedImg = prosImage.cannyImage(img_array)
    calcedRGB = prosImage.calcRGB(img_array)

    resultImage = utils.CV2toBase64(processedImg)

    print('image:',resultImage)
    pm = playSound.makeSound()
    # print(pm)
    audio_data = pm.fluidsynth()
    wavfile.write('test.wav',44100, audio_data)
    # pm.write('test.mid')
    f = open('test.wav','rb')
    buffer = f.read()
    print('music:',buffer)
    f.close()
    music = base64.b64encode(buffer).decode("utf-8")
    print('encodemusic:',music)
    add_muisc = "data:audio/midi;base64," + music
    print('added_music:',add_muisc)
    response = {
        'result': resultImage,
        'red'   : calcedRGB[0],
        'green' : calcedRGB[1],
        'blue'  : calcedRGB[2],
        'music' : add_muisc
    }
    return jsonify(response)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
        return render_template("index.html")
