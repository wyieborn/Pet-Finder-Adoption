from sklearn.model_selection import train_test_split
from Src import engine
from Configuration import config
    
    


def train_rf(df):
    cols_to_drop = ['AdoptionSpeed']
    X = df.drop(cols_to_drop, axis=1)
    y = df['AdoptionSpeed']
    engine.run_rf(X,y, config.GRIDCV_OPTION, None)    

    