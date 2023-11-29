from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
import joblib
from datetime import datetime
import os
from sklearn.pipeline import Pipeline

from Configuration import config
from Services import service
from Tuning import model_tuning
from Preprocess import processdata

model_path = config.MODEL_PATH
model_name = config.MODEL_NAME




def run_rf(X, y, grid_cv, model_save_path):
    Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.25, random_state=0)
    # Create a base model
    rf = RandomForestClassifier()
    model_pipeline =  processdata.data_encoding_pipeline() 
    try:
        if not os.path.exists(model_path):
            os.makedirs(model_path)
            print('{} directory created'.format(model_path))
        
        
            
        if not model_save_path:
            model_save_path='{}/{}'.format(model_path, model_name) # add versioning here
                
        if grid_cv:
            if not os.path.exists(model_save_path):
                print("Grid Search CV Started. Calculating Best Params-------------------------\n")
                model_ = Pipeline(steps=[('preprocessor', model_pipeline),
                        ('classifier', rf)]) 
                grid = model_tuning.compute_gscv(Xtrain, ytrain, model_, config.GRIDCV_PARAM)
                print("Grid Search CV completed-----------------------------------\n")
                print("Best Params are :",grid.best_estimator_)
                # Saving the best model to a file
                model = grid.best_estimator_
                joblib.dump(model, model_save_path)
                print(f"Best Random Forest model saved to {model_save_path}")
                

            else:
                print('Found a model\n')
                # Loading the pre-trained model from file
                model = joblib.load(model_save_path)
                print(f"Random Forest model loaded from {model_save_path}")
                
        else : 
            
            # model = Pipeline(steps=[('preprocessor', model_pipeline),
            #           ('classifier', 
            #            RandomForestClassifier(n_jobs=-1, n_estimators=200)
            #              )]) 
            model = Pipeline(steps=[('preprocessor', model_pipeline),
                      ('classifier', 
                    #    RandomForestClassifier(**config.RF_BEST_PARAMS)
                        RandomForestClassifier(n_jobs=-1, n_estimators=200)
                         )]) 
            model.fit(Xtrain, ytrain)
            joblib.dump(model, model_save_path)
            print(f"Random Forest model saved to {model_save_path}")
            
        eval_rf(model, Xtrain, Xtest, ytrain, ytest)
        return model
    
    except Exception as e:
        print('Exception :',e)
   
   
def eval_rf(model, Xtrain, Xtest, ytrain, ytest):
    y_model = model.predict(Xtest)
    y_model_train = model.predict(Xtrain)

    # Accuracy
    print("Random Forest Train Accuracy: ", accuracy_score(ytrain, y_model_train))
    print("Random Forest Test Accuracy: ", accuracy_score(ytest, y_model))
    
    if config.DEBUG:
        service.plot_confusion_matrix(y_model, ytest)
    
