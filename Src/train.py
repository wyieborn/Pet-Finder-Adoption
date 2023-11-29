from sklearn.model_selection import train_test_split
from Src import engine
from Configuration import config
    
    


def train_rf(df):
    cols_to_drop = ['AdoptionSpeed']
    X = df.drop(cols_to_drop, axis=1)
    y = df['AdoptionSpeed']
<<<<<<< HEAD
    model = engine.run_rf(X,y, config.GRIDCV_OPTION, None)    
    return model
=======
    engine.run_rf(X,y, config.GRIDCV_OPTION, None)    
>>>>>>> 8bc949e6ac3eff69a1d451a718948b0774f58406

    