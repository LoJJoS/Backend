from flask import Flask, request
import json
import os

from respond import Respond

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = ''# Change this to your credentials
os.environ['IMAGE_FOLDER'] = ''# Change to the output path
app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>API for FACEIT project</h1>'

@app.route('/create-image', methods=['POST'])
def create_image():
    result = {'status': 'OK'}
    token = request.args.get('room')
    if token is None:
        result['errmsg'] = 'No token provided'
        result['status'] = 'Error'
    else:
        if not request.is_json:
            result['errmsg'] = 'Invalid request'
            result['status'] = 'Error'
        else:
            data = request.json

            if 'imgs' not in data or not isinstance(data['imgs'], list):
                result['errmsg'] = 'No images provided / Need images need to be in a list'
                result['status'] = 'Error'
            else:
                try:
                    respond = Respond(data['imgs'])
                    result['result'] = respond.result_path
                    result['room']=token
                except Exception as e:
                    result['errmsg'] = str(e)
                    result['status'] = 'Error'
    return(json.dumps(result))

@app.route('/create-image-test', methods=['POST'])
def create_image_test():
    result = {'status': 'OK'}
    token = request.args.get('room')
    if token is None:
        result['errmsg'] = 'No token provided'
        result['status'] = 'Error'
    else:
        if not request.is_json:
            result['errmsg'] = 'Invalid request'
            result['status'] = 'Error'
        else:
            data = request.json

            if 'imgs' not in data or not isinstance(data['imgs'], list):
                result['errmsg'] = 'No images provided / Need images need to be in a list'
                result['status'] = 'Error'
            else:
                try:
                    for img in data['imgs']:
                        filefolder = os.environ['IMAGE_FOLDER'] 
                        if not os.path.isfile(f'{filefolder}/input/{img}'):
                            raise Exception('Image not found')
                    result['result'] = ['a3cefeae-011e-4cff-aafa-87dd719e8db5.png']
                    result['room']=token
                except Exception as e:
                    result['errmsg'] = str(e)
                    result['status'] = 'Error'
    return(json.dumps(result))
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)