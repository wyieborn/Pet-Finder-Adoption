import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import os
from Configuration import config

def load_data(data_dir):
    train_df = pd.read_csv(data_dir)
    return train_df


def plot_confusion_matrix(y_pred, y_test):

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy:.2f}')

    # Classification report and confusion matrix
    print(classification_report(y_test, y_pred))
    conf_matrix = confusion_matrix(y_test, y_pred)
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.show()
    
    
def create_model_folder(folder_path,tag):
    # new_path = 
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    pass

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_IMAGE_EXTENSIONS

def validate_data_type(data, contract):
    for field, data_type in contract.items():
        # if field not in data:
        #     raise ValueError(f"Missing field: {field}")
        if not isinstance(data[field], data_type):
            raise ValueError(f"Invalid data type for {field}, expected {data_type}")
        
def map_request_input(data, mapper):
    # validate_input(data, mapper)
    features_dict = {}
    for key, data_type in mapper.items():
        # print(key, data[key])
        if key in data:
        #     # Use the provided value if present
        #     value = int(data[key]) if data_type in [int, float] else data[key]
         # Use the provided value if present
            value = data[key]
            # Convert to the specified data type
            try:
                value = data_type(value)
            except (ValueError, TypeError):
                # Handle the case where conversion fails (e.g., '1.0' for int)
                value = None
        else:
            # Assign default values based on data type
            if data_type in [int, float]:
                value = 0
            else:
                value = ''

        features_dict[key] = value
    
    df = pd.DataFrame.from_dict([features_dict])
    print(df.head())
    return df

def validate_input():
    pass