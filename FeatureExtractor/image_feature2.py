import numpy as np # linear algebra
import pandas as pd
import os
import cv2
import numpy as np
import skimage.feature as skf
import skimage.filters as skg
from skimage.measure import shannon_entropy
from scipy.stats import entropy
from sklearn.cluster import KMeans

from Configuration import config

def extract_texture_features(img):
   
    # Convert the image to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    haralick = skf.graycomatrix(img_gray, [1], [0], 256, symmetric=True, normed=True) 
    energy = skf.graycoprops(haralick, 'energy')[0, 0] 
    contrast = skf.graycoprops(haralick, 'contrast')[0, 0] 
    correlation = skf.graycoprops(haralick, 'correlation')[0, 0] 
    entropy = shannon_entropy(img_gray)

    mean = np.mean(img)
    std_dev = np.std(img)

    return energy, contrast, correlation, entropy, mean, std_dev

def extract_keypoints(image):
    
    # Initialize the SIFT detector
    sift = cv2.SIFT_create()

    # Detect and compute SIFT keypoints and descriptors
    keypoints, _ = sift.detectAndCompute(image, None)

    # Return the number of keypoints
    return len(keypoints)

def extract_and_update(row):
    file_path = os.path.join(config.TRAIN_IMAGE_DIR, f"{row['PetID']}.jpg")
    # Load an image
    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

    num_keypoints = extract_keypoints(image)
    return num_keypoints

def extract_train_feat():
    if not os.path.exists(config.IMG_FEAT2):
        # looping through the training images
        # Create an empty dataframe
        df_train_img = pd.DataFrame(columns=['PetID', 'Energy', 'Contrast', 'Correlation', 'Entropy', 'Mean', 'Std_Dev'])

        # Loop through each image in the folder
        for filename in os.listdir(config.TRAIN_IMAGE_DIR):
            if filename.endswith('.jpg'):
                # Extract the texture features
                image_path = os.path.join(config.TRAIN_IMAGE_DIR, filename)
                img = cv2.imread(image_path)
                energy, contrast, correlation, entropy, mean, std_dev = extract_texture_features(img)
                
                # Add the features to the dataframe
                df_train_img = pd.concat([df_train_img, pd.DataFrame({'PetID': [filename[:-4]], 'Energy': [energy], 'Contrast': [contrast], 'Correlation': [correlation], 'Entropy': [entropy], 'Mean': [mean], 'Std_Dev': [std_dev]})])
        # Update the 'num_checkpoints' column
        df_train_img['num_checkpoints'] = df_train_img.apply(extract_and_update, axis=1)
        
        # Columns to drop
        columns_to_drop = ['mean_h', 'mean_s', 'mean_v', 'variance_h', 'variance_s', 'variance_v']

        # Drop specified columns
        df_train_img = df_train_img.drop(columns=columns_to_drop, errors='ignore')

    else:
        print('Saved image features found .........')
        df_train_img = pd.read_csv(config.IMG_FEAT2, index_col=0)
    # print(df_train_img.head())
    return df_train_img





def extract_image_features(img):
    img_feat = extract_texture_features(img)
    columns = ['Energy', 'Contrast', 'Correlation', 'Entropy', 'Mean', 'Std_Dev']
    df = pd.DataFrame([img_feat], columns=columns)
    df['num_checkpoints'] = extract_keypoints(img)
    return df

