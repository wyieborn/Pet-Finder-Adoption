
from Preprocess import processdata
from Services import service

data_dir = 'data'



if __name__ == '__main__':
    
    numerical, categorical, img, text   = service.load_data(data_dir)
    final_dataframe = processdata.process(numerical, categorical,img, text)
    print(final_dataframe)