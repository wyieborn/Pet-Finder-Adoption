import streamlit as st
import requests


# Sample data for pet images and their details
pet_data = [
    {
        "Type": "Cat",
        "Name": "Kitty",
        "Age": 12,
        "Breed1": 265,
        "Breed2": 0,
        "Gender": 2,
        "Color1": 1,
        "Color2": 7,
        "Color3": 0,
        "MaturitySize": 2,
        "FurLength": 2,
        "Vaccinated": 3,
        "Dewormed": 3,
        "Sterilized": 3,
        "Health": 1,
        "Quantity": 1,
        "Fee": 0,
        "Description": "Very manja and gentle stray cat found, we would really like to find a home for it because we cannot keep her for ourselves for long. Has a very cute high pitch but soft meow. Please contact me if you would be interested in adopting.",
        "PhotoAmt": 2,
    },
    {
        "Type": "Cat",
        "Name": "No Name Yet",
        "Age": 1,
        "Breed1": 265,
        "Breed2": 0,
        "Gender": 1,
        "Color1": 1,
        "Color2": 2,
        "Color3": 0,
        "MaturitySize": 2,
        "FurLength": 2,
        "Vaccinated": 3,
        "Dewormed": 3,
        "Sterilized": 3,
        "Health": 1,
        "Quantity": 1,
        "Fee": 0,
        "Description": "I just found it alone yesterday near my apartment. It was shaking so I had to bring it home to provide temporary care.",
        "PhotoAmt": 2,
    },
]


def show_image_click_game():
    st.title("Which Pet is More Likely to Get Adopted?")
    st.write("Click on the pet that you think is more likely to get adopted.")

    col1, col2 = st.columns(2)

    # Get adoptability predictions for Pet 1 and Pet 2 from the provided pet data list
    response_1 = requests.post("http://localhost:5000/predict", data=pet_data[0])
    response_2 = requests.post("http://localhost:5000/predict", data=pet_data[1])

    pet_1_prediction = int(
        response_1.json().get("predictions") if response_1.status_code == 200 else None
    )
    pet_2_prediction = int(
        response_2.json().get("predictions") if response_2.status_code == 200 else None
    )
    with col1:
        img1 = "cat2.jpg"  # Replace this with the actual image path or URL
        st.image(img1, use_column_width=True, output_format="JPEG")
        # st.write(f"Type: Cat")
        # st.write(f"Age: 1.5 years")
        # st.write(f"Health: Healthy")

        if st.button("Pet 1"):
            # Display the result based on the comparison of predictions
            if pet_1_prediction is not None and pet_2_prediction is not None:
                if pet_1_prediction < pet_2_prediction:
                    st.success("Correct! Pet 1 is more likely to get adopted.")
                else:
                    st.error("Oops! Pet 1 might not be as likely to get adopted.")

    with col2:
        img2 = "cat1.jpg"
        st.image(img2, use_column_width=True, output_format="JPEG")
        # st.write(f"Type: Cat")
        # st.write(f"Age: 2 years")
        # st.write(f"Health: Not Healthy")
        if st.button("Pet 2"):
            if pet_1_prediction is not None and pet_2_prediction is not None:
                if pet_2_prediction < pet_1_prediction:
                    st.success("Correct! Pet 2 is more likely to get adopted.")
                else:
                    st.error("Oops! Pet 2 might not be as likely to get adopted.")


def display_image(image_filename):
    try:
        st.image(image_filename, use_column_width=True)
    except FileNotFoundError:
        st.error("Image not found. Please provide the correct image filename.")


def get_user_input(fields):
    user_data = {}
    num_columns = 2
    columns = st.columns(num_columns)
    num_files_uploaded = 0

    for idx, (field, options) in enumerate(fields.items()):
        field_type = options["type"]
        required = options["required"]
        default_value = options.get("default_value")

        if field_type == "file":
            uploaded_file = st.file_uploader(
                f"Choose {field.lower()}", type=["jpg", "jpeg", "png"]
            )
            if uploaded_file is not None:
                num_files_uploaded += 1
                user_data[field] = uploaded_file
        elif field_type in ["text", "number"]:
            user_data[field] = (
                columns[idx % num_columns].text_input(
                    f"Enter {field}{'*' if required else ''}", ""
                )
                if field_type == "text"
                else columns[idx % num_columns].number_input(
                    f"Enter {field}{'*' if required else ''}", value=default_value or 0
                )
            )
        elif field_type == "selectbox":
            selected_value = columns[idx % num_columns].selectbox(
                f"Select {field}{'*' if required else ''}", options=options["options"]
            )
            user_data[field] = selected_value

    user_data["PhotoAmt"] = num_files_uploaded

    return user_data


def process_data(user_data, fields):
    for field in ["Gender", "Vaccinated", "Dewormed", "Sterilized"]:
        if field == "Gender":
            user_data[field] = 1 if user_data.get(field) == "Male" else 2
        else:
            field_value = user_data.get(field)
            if field_value == "Yes":
                user_data[field] = 1
            elif field_value == "No":
                user_data[field] = 2
            elif field_value == "Not Sure":
                user_data[field] = 3

    # Mapping for Color
    color_mapping = {
        "None": 0,
        "Black": 1,
        "Brown": 2,
        "Golden": 3,
        "Yellow": 4,
        "Cream": 5,
        "Gray": 6,
        "White": 7,
    }

    user_data["Color1"] = color_mapping.get(user_data.get("Color1"))
    user_data["Color2"] = color_mapping.get(user_data.get("Color2"))
    user_data["Color3"] = color_mapping.get(user_data.get("Color3"))

    # Mapping for Health
    health_mapping = {
        "Not Specified": 0,
        "Healthy": 1,
        "Minor Injury": 2,
        "Serious Injury": 3,
    }
    user_data["Health"] = health_mapping.get(user_data.get("Health"))

    type_mapping = {"Cat": 2, "Dog": 1}
    
    user_data["Type"] = type_mapping.get(user_data.get("Type"))

    # Mapping for MaturitySize
    maturity_mapping = {
        "Not Specified": 0,
        "Small": 1,
        "Medium": 2,
        "Large": 3,
        "Extra Large": 4,
    }
    user_data["MaturitySize"] = maturity_mapping.get(user_data.get("MaturitySize"))

    # Mapping for FurLength
    fur_mapping = {"Not Specified": 0, "Short": 1, "Medium": 2, "Long": 3}
    user_data["FurLength"] = fur_mapping.get(user_data.get("FurLength"))

    required_fields = [
        field
        for field, options in fields.items()
        if options["required"]
        and (
            user_data.get(field) is None
            or (isinstance(user_data.get(field), str) and user_data.get(field) == "")
        )
    ]

    boolean_required_fields = ["Vaccinated", "Dewormed", "Sterilized"]
    for field in boolean_required_fields:
        if field in user_data and isinstance(user_data[field], int):
            continue
        required_fields.append(field)

    return required_fields


def display_required_fields_warnings(required_fields):
    if required_fields:
        st.warning("Please fill in all mandatory fields.")
        for field in required_fields:
            st.markdown(
                f"<span style='color:red'>Required field: {field}</span>",
                unsafe_allow_html=True,
            )


def display_additional_info(response):
    additional_info = f"Response {response}"
    st.write(additional_info)


def show_home_page():
    img_filename = "logo.png"
    display_image(img_filename)
    st.title("Pet Find Adoption")

    fields = {
        "Image": {"type": "file", "required": False},
        "Type": {"type": "selectbox", "options": ["1-Dog", "2-Cat"], "required": True},
        "Name": {"type": "text", "required": True},
        "Age": {"type": "number", "required": True},
        "Gender": {
            "type": "selectbox",
            "options": ["Male", "Female"],
            "required": True,
        },
        "Breed1": {"type": "number", "required": False, "default_value": 0},
        "Breed2": {"type": "number", "required": False, "default_value": 0},
        "Color1": {
            "type": "selectbox",
            "options": [
                "None",
                "Black",
                "Brown",
                "Golden",
                "Yellow",
                "Cream",
                "Gray",
                "White",
            ],
            "required": True,
        },
        "Color2": {
            "type": "selectbox",
            "options": [
                "None",
                "Black",
                "Brown",
                "Golden",
                "Yellow",
                "Cream",
                "Gray",
                "White",
            ],
            "required": True,
        },
        "Color3": {
            "type": "selectbox",
            "options": [
                "None",
                "Black",
                "Brown",
                "Golden",
                "Yellow",
                "Cream",
                "Gray",
                "White",
            ],
            "required": True,
        },
        "MaturitySize": {
            "type": "selectbox",
            "options": ["Not Specified", "Small", "Medium", "Large", "Extra Large"],
            "required": True,
        },
        "FurLength": {
            "type": "selectbox",
            "options": ["Not Specified", "Short", "Medium", "Long"],
            "required": True,
        },
        "Vaccinated": {
            "type": "selectbox",
            "options": ["Not Sure", "Yes", "No"],
            "required": True,
        },
        "Dewormed": {
            "type": "selectbox",
            "options": ["Not Sure", "Yes", "No"],
            "required": True,
        },
        "Sterilized": {
            "type": "selectbox",
            "options": ["Not Sure", "Yes", "No"],
            "required": True,
        },
        "Health": {
            "type": "selectbox",
            "options": ["Not Specified", "Healthy", "Minor Injury", "Serious Injury"],
            "required": True,
        },
        "Quantity": {"type": "number", "required": True},
        "Fee": {"type": "number", "required": True},
        "Description": {"type": "text", "required": True},
    }

    user_data = get_user_input(fields)
    if st.button("Predict"):
        print(user_data)
        required_fields = process_data(user_data, fields)

        # st.title(user_data)
        display_required_fields_warnings(required_fields)
        if not required_fields:
            with st.spinner("Processing data..."):
                response = requests.post(
                    "http://localhost:5000/predict", data=user_data
                )
                if response.status_code == 200:
                    # st.title(response.text)
                    prediction = int(response.json().get("predictions"))
                    if prediction == 0:
                        st.success("This pet has the highest chance of being adopted.")
                    elif 1 <= prediction <= 3:
                        st.warning("This pet has a good chance of being adopted.")
                    elif prediction == 4:
                        st.error("This pet has a low chance of being adopted.")
                        st.write(
                            "Please contact the following organizations for ensuring a safe home for this pet."
                        )
                        contact_info = [
                            ["Organization", "Contact Number", "Email Address"],
                            [
                                "Ontario SPCA and Humane Society",
                                "1-888-668-7722",
                                "info@ontariospca.ca",
                            ],
                            [
                                "Animal Services Shelter - City of Mississauga",
                                "311 (905-615-4311 outside City limits)",
                                "mypet.info@mississauga.ca",
                            ],
                            [
                                "Animal Shelters - Alberta SPCA",
                                "+1 800-455-9003",
                                "donorrelations@albertaspca.org",
                            ],
                            [
                                "Dartmouth Shelter - Nova Scotia SPCA",
                                "902-468-7877 or 1-844-835-4798",
                                "dartmouth@spcans.ca",
                            ],
                            [
                                "Redemption Paws",
                                "902-345-7586",
                                "info@redemptionpaws.org",
                            ],
                        ]
                        st.table(contact_info)
                    else:
                        st.warning("Prediction value out of range.")

                    # expander = st.expander("Additional Information", expanded=False)
                    # with expander:
                    #     display_additional_info(response)

                else:
                    st.error("Failed to process data. Please try again.")
                    st.text(f"Response from server: {response.text}")


def show_about_page():
    # Title and introductory text
    st.title("AI-Powered Pet Adoption Optimizer")
    st.write("Welcome to our project aimed at revolutionizing pet adoptions!")

    # Description
    st.write(
        "We are a passionate team of university students driven by a shared vision: to leverage the capabilities of machine learning to optimize pet adoptions. Our project is not just an academic exercise; it's a practical application of cutting-edge technology in the service of animal welfare."
    )

    # Features of the system
    st.header("Our System Features")
    st.write(
        '- Automatically analyze pet attributes to compute an "adoptability score".'
    )
    st.write(
        "- Predict the likelihood of a pet getting adopted based on historical data."
    )
    st.write(
        "- Expand the search globally for pets with low adoption likelihood locally."
    )
    st.write(
        "- Identify shelters and families in other geographies where pets have a higher chance of finding a home."
    )

    # Our Mission
    st.header("Our Mission")
    st.write(
        "Our primary goal is to create an intelligent system that empowers animal shelters and rescue organizations to significantly enhance their adoption rates. By developing advanced algorithms that meticulously analyze various attributes of pets, such as breed, age, medical status, and personality traits, we compute an 'adoptability score.' This score predicts the likelihood of a pet finding a loving home based on comprehensive historical data."
    )

    st.header("Taking Adoption Global")
    st.write(
        "Going beyond the local scope, our system doesn't stop at predicting adoptability. For pets that might face challenges in finding a home locally, we've incorporated a feature that expands the search globally. This involves scouring databases worldwide to pinpoint shelters, foster agencies, and families in other regions where a particular pet stands a higher chance of finding a perfect match. This innovative approach broadens opportunities for animals to connect with the right guardians, regardless of geographical constraints."
    )

    st.header("Our Vision")
    st.write(
        "We are committed to applying our academic knowledge practically. By utilizing AI to optimize pet adoptions, we aspire to create a meaningful impact on animal welfare, not just within our immediate community but also on a global scale. Our values of compassion and innovation drive us to harness technology for the greater good."
    )

    st.header("Contact Us")
    st.write("Email: groupSix@mylambton.ca")
    st.write("Phone: +1 234567890")

    # Disclaimer
    st.write(
        "Please note: This is a simplified representation of our project for demonstration purposes. For a comprehensive understanding, contact us for detailed information."
    )

    show_image_click_game()


def main():
    selected_page = st.sidebar.selectbox("Select Page", ["About Us", "Application"])

    if selected_page == "About Us":
        show_about_page()
    elif selected_page == "Application":
        show_home_page()


if __name__ == "__main__":
    main()
