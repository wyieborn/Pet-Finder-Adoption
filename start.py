
from Preprocess import processdata
from Services import service
from Configuration import config
from Src import train

train_dir = config.TRAIN_DIR
image_dir = config.TRAIN_IMAGE_DIR

if __name__ == '__main__':
    
    df   = service.load_data(train_dir)
    final_dataframe = processdata.process(df, image_dir)
    
    train.train_rf(final_dataframe)
