
DEBUG = False

ROOT_DIR = 'data'
TRAIN_DIR = 'data/train/train.csv'
TRAIN_IMAGE_DIR = 'data/train_images'
TRAIN_METADATA = 'data/train_metadata'
BREED_LABELS_DIR = 'data/breed_labels.csv'
COLOR_LABELS_DIR = 'data/color_labels.csv'
STATE_LABELS = 'data/state_labels.csv'

MODEL_PATH = 'Models'
MODEL_NAME = 'random_forest_model_v2.joblib'

# DENSENET CONFIG HERE
TRAIN_BATCH_SIZE = 16
VALID_BATCH_SIZE = 8
EPOCHS = 10  


# RANDOM FOREST
GRIDCV_OPTION = False
RF_BEST_PARAMS = {
                    # 'n_jobs' : -1,
                    'bootstrap': True,
                    'max_depth': 120,
                    'min_samples_leaf': 3,
                    'min_samples_split': 8,
                    'n_estimators': 200
                }
GRIDCV_PARAM  = {
     
        'classifier__bootstrap': [True],  # Method of selecting samples for training each tree
        'classifier__max_depth': [120, 140, 150, 160],  # Maximum number of levels in tree
        'classifier__min_samples_leaf': [3, 4, 5],  # Minimum number of samples required at each leaf node
        'classifier__min_samples_split': [8, 10, 12],  # Minimum number of samples required to split a node
        'classifier__n_estimators': [100, 200, 300]  # Number of trees in random forest
    }

# allowed file extensions for image uploads
ALLOWED_IMAGE_EXTENSIONS = {
                        'png', 
                        'jpg', 
                        'jpeg', 
                        'gif'
                    }

# base input data structure and datatype
INPUT_MODEL = {
    'Type' : str,
    'Name' : str,
    'Age' : int,
    'Breed1' : int,
    'Breed2': int,
    'Gender' : int,
    'Color1' : int,
    'Color2' : int,
    'Color3' : int,
    'MaturitySize': int,
    'FurLength' : int,
    'Vaccinated' : int,
    'Dewormed' : int,
    'Sterilized' : int,
    'Health' : int,
    'Quantity' : int,
    'Fee' : int,
    'State' : int,
    'RescuerID' : object,
    'VideoAmt' : int,
    'Description' : str,
    'PetID' : object,
    'PhotoAmt' : float
    }

IMG_FEAT2 = 'image_features2.csv'