from flask import Flask, request, jsonify
from functools import lru_cache
import joblib
import pandas as pd
import os
import cv2
from PIL import Image
import numpy as np
from Configuration import config
from Services import service
from Preprocess import processdata
import start

app = Flask(__name__)




@lru_cache(maxsize=1)  # Caching the result of load_model for subsequent calls
def load_model():
    path = '{}/{}'.format(config.MODEL_PATH,config.MODEL_NAME)
    if os.path.exists(path):
        print('Loading saved model from cache.....')
        model = joblib.load(path) 
        print('Loading successfull.....') 
        return model
    else:
        print('Training Started.........')
        model = start.train_model()
        print('Training Completed..........')
        return model

def prepare_features(request):
    # Check if the POST request has the 'image' file or 'data' fields
    # --------------------
    if 'image' not in request.files and len(request.form) <= 0:
        return jsonify({'error': 'Image file or data fields are required for prediction.'})
        
    # # Getting the image file and data from the request 
    if len(request.files)>0:
        image_file = request.files['image']
        # Checking if the image file is allowed
        if image_file.filename == '' or not service.allowed_file(image_file.filename):
            return jsonify({'error': 'Invalid image file format.'})

        # # Reading the image file and extracting features
        # img = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
        img = Image.open(image_file)
        img_array = np.array(img)
        # get image features here
        # df_image = get_image_features(img_array)
    else:
        img_array = None
    

    df = service.map_request_input(request.form, config.INPUT_MODEL)

    # process df
    df = processdata.process(df, img_array)

    return df
    
# Flask route for making predictions
@app.route('/predict', methods=['POST'])
# @app.route('/predict')
def predict():
    try:
        # Get the input data from the request
        # data = request.get_json()
        # for query parameter
        # data = request.args.get('data')    


        # # Load the machine learning model
        model = load_model()
        # prepare our data
        df = prepare_features(request)
        # # Make predictions using the model
        prediction = model.predict(df)
        # Return the predictions
        # return jsonify({'prediction': prediction.tolist()})
        return jsonify({
                        'predictions': str(prediction[0]),
                        # 'model' : model.name
                        
                        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run()
