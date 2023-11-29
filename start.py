
from Preprocess import processdata
from Services import service
from Configuration import config
from Src import train

train_dir = config.TRAIN_DIR
image_dir = config.TRAIN_IMAGE_DIR



def train_model():
    df   = service.load_data(train_dir)
    print('Feature Processing Started...............')

    final_dataframe = processdata.process_train(df)
    print('Training Initiated...............')

    model = train.train_rf(final_dataframe)
    
    return model
    
def predict_data(df, img):
    final_dataframe = processdata.process(df, image_dir) 
    pass


if __name__ == '__main__':
    
    train_model()