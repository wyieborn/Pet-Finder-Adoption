# Pet-Finder-Adoption

## Setting up the application

1. Configure required paths in Configuration-> config.py. Adjust below paths:
   - data path( train csv path is must; image path required when no pre-computed img feature is present).
   - img feature path( optional - but saves lot of time) - currently fetches from app's root directory,
   - model path and name( optional- required when using your own model).
     
     Optional :
     - To train the model while computing image features; use "python start.py()" after configuring above path as it takes too long and there is a session timeout between apps.
     - To view confusion matrix and performance, set DEBUG = TRUE
    
      
2. Initiate Flask api using "python app.py"
3. Run streamlit application using "streamlit run streamlit_app.py" and test the app.
4. If any error drop a message.
