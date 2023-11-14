from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
import joblib
from datetime import datetime
import os

from Configuration import config
from Services import service

model_path = config.MODEL_PATH

def compute_gscv(X,y):
    # Create the parameter grid based on the results of random search 
    param_grid = {
        'bootstrap': [True],               # Method of selecting samples for training each tree
        'max_depth': [120, 140, 150, 160], # Maximum number of levels in tree
        #'max_features': [3, 4, 5],        # Number of features to consider at every split
        'min_samples_leaf': [3, 4, 5],     # Minimum number of samples required at each leaf node
        'min_samples_split': [8, 10, 12],  # Minimum number of samples required to split a node
        'n_estimators': [100, 200, 300]    # Number of trees in random forest
    }
    # Create a based model
    rf = RandomForestClassifier()
    # Instantiate the grid search model
    grid = GridSearchCV(estimator = rf, param_grid = param_grid, 
                            cv = 3, n_jobs = -1, verbose = 2)
    grid.fit(X, y)
    return grid


def run_rf(X, y, grid_cv, model_save_path):
    Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.25, random_state=0)

    
    try:
        if not os.path.exists(model_path):
            os.makedirs(model_path)
            print('{} directory created'.format(model_path))
        
        
            
        if not model_save_path:
            model_save_path='{}/random_forest_model.joblib'.format(model_path) # add versioning here
                
        if grid_cv:
            if not os.path.exists(model_save_path):
                print("Grid Search CV Started. Calculating Best Params-------------------------\n")
                grid = compute_gscv(X, y)
                print("Grid Search CV completed-----------------------------------\n")
                # Saving the best model to a file
                joblib.dump(grid.best_estimator_, model_save_path)
                print(f"Best Random Forest model saved to {model_save_path}")
                model = grid.best_estimator_

            else:
                print('Found a model\n')
                # Loading the pre-trained model from file
                model = joblib.load(model_save_path)
                print(f"Random Forest model loaded from {model_save_path}")
                
                
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
    
    service.plot_confusion_matrix(y_model, ytest)
    
