
from sklearn.model_selection import GridSearchCV
from Configuration import config

def compute_gscv(X,y, model, param_grid):
    if not param_grid:
        # Create the parameter grid based on the results of random search 
        param_grid = config.RF_BEST_PARAMS
    # Instantiate the grid search model
    grid = GridSearchCV(estimator = model, param_grid = param_grid, 
                            cv = 3, n_jobs = -1, verbose = 2)
    grid.fit(X, y)
    return grid