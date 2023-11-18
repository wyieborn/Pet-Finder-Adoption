

ROOT_DIR = 'data'
TRAIN_DIR = 'data/train/train.csv'
TRAIN_IMAGE_DIR = 'data/train_images'
TRAIN_METADATA = 'data/train_metadata'
BREED_LABELS_DIR = 'input/breed_labels.csv'
COLOR_LABELS_DIR = 'input/color_labels.csv'
STATE_LABELS = 'input/state_labels.csv'

MODEL_PATH = 'Models'

# DENSENET CONFIG HERE
TRAIN_BATCH_SIZE = 16
VALID_BATCH_SIZE = 8
EPOCHS = 10  


# RANDOM FOREST
RF_BEST_PARAMS = {
                    'bootstrap': True,
                    'max_depth': 120,
                    'min_samples_leaf': 3,
                    'min_samples_split': 8,
                    'n_estimators': 200
                }

