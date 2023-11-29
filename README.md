# Pet-Finder-Adoption

## Setting up the application


1. Configure required paths in Configuration-> config.py. Adjust below paths:
   - data path( train csv path is must; image path required when no pre-computed img feature is present).
   - img feature path( optional - but saves lot of time) - currently fetches from app's root directory. Example : IMG_FEAT2 = 'image_features.csv' works after moving it to root dir.
   - model path and name( optional- required when using your own model).
     
     Optional :
     - To train the model while computing image features; use "python start.py()" after configuring above path as it takes too long and there is a session timeout between apps.
     - To view confusion matrix and performance, set DEBUG = TRUE
    
2. Install required python packages using "pip install -r requirements.txt" after navigating to its folder( virtual environment recommended ).
3. Initiate Flask api using "python app.py" to serve the streamlit application.
4. Run streamlit application using "streamlit run streamlit_app.py".
5. If any error drop a message.
