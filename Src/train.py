from sklearn.model_selection import train_test_split
from Src import engine

    
    


def train_rf(df):
    cols_to_drop = ['PetID', 'AdoptionSpeed','Description','Name','RescuerID']
    X = df.drop(cols_to_drop, axis=1)
    y = df['AdoptionSpeed']
    engine.run_rf(X,y, True, None)    

    