from FeatureExtractor import image_feature, text_features, image_feature2
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import torch
from textblob import TextBlob
import numpy as np
np.seterr(divide='ignore', invalid='ignore')

def image_resize():
    pass



def get_text_features(text):
    pass



def get_new_features(df):
    # Creating a new feature based on the length of the description
    df['Description_Length'] = df['Description'].apply(lambda x: len(str(x)))

    # Creating a feature indicating whether a pet has a name or not
    df['HasName'] = df['Name'].apply(lambda x: 0 if pd.isnull(x) else 1)
    
    # Adding features engineering for df dataset
    to_scale = ['AgeScaled']
    scale_num = ['Age']
    df[to_scale] = ((df[scale_num] - df[scale_num].mean()) / df[scale_num].std()).fillna(0)
    # Concatenating Breed1, Age and Furlength features
    df['Breed1AgeFurLength'] = (df['Breed1'].astype(str) + np.abs(df['AgeScaled']).astype(str) + df['FurLength'].astype(str)).astype(float)
    df['Breed2AgeFurLength'] = (df['Breed2'].astype(str) + np.abs(df['AgeScaled']).astype(str) + df['FurLength'].astype(str)).astype(float)

    # Concatenating binary features such as Vaccinated, Dewormed and Sterilized
    df['VDSCombination'] = (df['Vaccinated'].astype(str) + df['Dewormed'].astype(str) + df['Sterilized'].astype(str)).astype(float)

    # Creating a color count feature without including cases where any color is 0
    df['ColorCount'] = df[['Color1', 'Color2', 'Color3']].apply(lambda row: len([color for color in row if color != 0]), axis=1)

    # Creating a total visual media feature
    df['TotalVisualMedia'] = df['PhotoAmt'] + df['VideoAmt']

    # Creating a description length feature
    df['DescriptionLength'] = df['Description'].apply(lambda x: len(str(x)))

    # Creating a sentiment score feature
    df['SentimentScore'] = df['Description'].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
    df['Subjectivity'] = df['Description'].apply(lambda x: TextBlob(str(x)).sentiment.subjectivity)
    
    #Name_word_len, 'RescuerID_3', 'RescuerID_5', 'Description_len', 'PhotoAmt', 'Name_word_len', 'is_emoji'
    df['Name_word_len'] = df['Name'].fillna('').apply(lambda x : len(x.split(' ')))


    return df



def data_encoding_pipeline():
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

def process_train(df):
    
    img_df = image_feature2.extract_train_feat()
    img_df['PetID'] = img_df['PetID'].apply(lambda x : x.split('-')[0])
    
    img_features = image_feature.process_image_train()
    
    df = get_new_features(df)
    
    #combine and return
    merged_df = pd.merge(df, img_df, how="inner", on=["PetID"], copy=True)
    merged_df = merged_df.merge(img_features, how='left', on='PetID')
    cols_to_drop = ['PetID', 'Description', 'Name','RescuerID', 'AgeScaled']
    merged_df = merged_df.drop(cols_to_drop, axis = 1)
    
    
    
    # merged_df = df
    merged_df = merged_df.fillna(0)
    print(merged_df.head())
    return merged_df

def process(df, img):

    if img is not None:
        img_array = np.array(img)
        img_df = image_feature2.extract_image_features(img_array)
        
        img_nn = image_feature.process_image(img)
        nn_df = pd.DataFrame(img_nn)

        img_df = pd.concat([img_df, nn_df], axis=1)

    else:
        img_df = None
        
    df = get_new_features(df)
    
    #combine and return
    # merged_df = pd.merge(feat_, img_feat, on='pet_id', how='left')
    merged_df = pd.concat([df, img_df], axis=1)

    
    cols_to_drop = ['Description', 'Name','RescuerID', 'AgeScaled']
    merged_df = merged_df.drop(cols_to_drop, axis = 1)
    merged_df = merged_df.fillna(0)
    
    print(merged_df)
    return merged_df