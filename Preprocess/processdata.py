from FeatureExtractor import image_feature, text_features
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import torch

def image_resize():
    pass

def process_image_features(img=torch.rand((1,3,256,256))):
    img_feat = image_feature.get_image_features(img)
    return img_feat

def process_text_features(text):
    pass

def get_new_features(df):
    # Creating a new feature based on the length of the description
    df['Description_Length'] = df['Description'].apply(lambda x: len(str(x)))

    # Creating a feature indicating whether a pet has a name or not
    df['HasName'] = df['Name'].apply(lambda x: 0 if pd.isnull(x) else 1)
    
    return df



def data_encoding(df):
    # encoding categorical data and create pipeline for automating the process for new data
    numeric_features = ['Age','Fee','VideoAmt','PhotoAmt','Quantity']
    
    categorical_features = ['Type', 'Color1', 'Color2', 'Gender', 'MaturitySize', 
                        'FurLength', 'Vaccinated', 'Sterilized', 'Health', 'Breed1','Gender']
    
    numeric_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())])


    categorical_transformer = Pipeline(steps=[
        
        ('onehot', OneHotEncoder(handle_unknown='ignore'))])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)])
    
    return preprocessor

def process(df, img):
    # img_feat = process_image_features(img)
    feat_ = get_new_features(df)
    
    #combine and return
    # merged_df = pd.merge(feat_, img_feat, on='pet_id', how='left')
    merged_df = feat_
    
    return merged_df

