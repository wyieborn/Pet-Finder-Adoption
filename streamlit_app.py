import streamlit as st
import requests

# Upload image function
def upload_image():
    uploaded_file = st.file_uploader("Choose an image...", type="jpg")
    return uploaded_file


# Streamlit UI
def main():
    st.title("PET-FINDER PROTOTYPE")

    # Get user input
    type = st.text_input("Enter Type:", value = -1, key = 'type')
    name = st.text_input("Enter Name:", value = '', key = 'name')

    # Upload image
    image_file = upload_image()

    # Button to trigger the upload
    if st.button("Predict"):
        if image_file is not None:
            # Prepare data for POST request
            files = {'image': image_file}
            data = {'Type': type, 'Name': name}

            # Make a POST request to Flask server
            response = requests.post("http://localhost:5000/predict", files=files, data=data)

            # Display response from Flask server
            st.text(f"Response from server: {response.text}")
        else :
            data = {'Type': type, 'Name': name}
            # Make a POST request to Flask server
            response = requests.post("http://localhost:5000/predict", data=data)

            # Display response from Flask server
            st.text(f"Response from server: {response.text}")

if __name__ == "__main__":
    main()
