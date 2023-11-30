import streamlit as st
import requests


def display_image(image_filename):
    try:
        st.image(image_filename, use_column_width=True)
    except FileNotFoundError:
        st.error("Image not found. Please provide the correct image filename.")


def get_user_input(fields):
    user_data = {}
    num_columns = 2
    columns = st.columns(num_columns)

    for idx, (field, options) in enumerate(fields.items()):
        field_type = options["type"]
        required = options["required"]

        if field_type == "file":
            user_data[field] = st.file_uploader(
                f"Choose {field.lower()}", type=["jpg", "jpeg", "png"]
            )
        elif field_type in ["text", "number"]:
            user_data[field] = (
                columns[idx % num_columns].text_input(
                    f"Enter {field}{'*' if required else ''}", ""
                )
                if field_type == "text"
                else columns[idx % num_columns].number_input(
                    f"Enter {field}{'*' if required else ''}", value=0
                )
            )
        elif field_type == "selectbox":
            selected_value = columns[idx % num_columns].selectbox(
                f"Select {field}{'*' if required else ''}", options=options["options"]
            )
            user_data[field] = selected_value

    return user_data


def process_data(user_data, fields):
    for field in ["Gender", "Vaccinated", "Dewormed", "Sterilized"]:
        if field == "Gender":
            user_data[field] = 1 if user_data.get(field) == "Male" else 2
        else:
            user_data[field] = 1 if user_data.get(field) == "Yes" else 0

    # Mapping for Color
    color_mapping = {
        "Red": 1,
        "Blue": 2,
        "Green": 3,
        "Yellow": 4,
        "White": 5,
        "Black": 6,
        "Brown": 7,
        "Orange": 8,
        "Gray": 9,
        "Purple": 10,
        "Pink": 11,
        "Gold": 12,
    }
    user_data["Color1"] = color_mapping.get(user_data.get("Color1"))
    user_data["Color2"] = color_mapping.get(user_data.get("Color2"))
    user_data["Color3"] = color_mapping.get(user_data.get("Color3"))

    # Mapping for State
    state_mapping = {"State A": 1, "State B": 2, "State C": 3, "State D": 4}
    user_data["State"] = state_mapping.get(user_data.get("State"))

    # Mapping for Health
    health_mapping = {"Healthy": 1, "Minor Injury": 2, "Serious Injury": 3}
    user_data["Health"] = health_mapping.get(user_data.get("Health"))

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


def main():
    img_filename = "logo.png"
    display_image(img_filename)
    st.title("Pet Find Adoption")

    fields = {
        "Image": {"type": "file", "required": True},
        "Type": {"type": "text", "required": True},
        "Name": {"type": "text", "required": True},
        "Age": {"type": "number", "required": True},
        "Gender": {
            "type": "selectbox",
            "options": ["Male", "Female"],
            "required": True,
        },
        "Breed1": {"type": "text", "required": False},
        "Breed2": {"type": "text", "required": False},
        "Color1": {
            "type": "selectbox",
            "options": ["Red", "Blue", "Green", "Yellow"],
            "required": True,
        },
        "Color2": {
            "type": "selectbox",
            "options": ["White", "Black", "Brown", "Orange"],
            "required": True,
        },
        "Color3": {
            "type": "selectbox",
            "options": ["Gray", "Purple", "Pink", "Gold"],
            "required": True,
        },
        "MaturitySize": {"type": "number", "required": True},
        "FurLength": {"type": "number", "required": True},
        "Vaccinated": {"type": "selectbox", "options": ["Yes", "No"], "required": True},
        "Dewormed": {"type": "selectbox", "options": ["Yes", "No"], "required": True},
        "Sterilized": {"type": "selectbox", "options": ["Yes", "No"], "required": True},
        "Health": {
            "type": "selectbox",
            "options": ["Healthy", "Minor Injury", "Serious Injury"],
            "required": True,
        },
        "Quantity": {"type": "number", "required": True},
        "Fee": {"type": "number", "required": True},
        "State": {
            "type": "selectbox",
            "options": ["State A", "State B", "State C", "State D"],
            "required": True,
        },
        "Description": {"type": "text", "required": True},
        "PhotoAmt": {"type": "number", "required": True},
    }

    def display_additional_info():
        additional_info = "Additional information goes here."
        st.write(additional_info)

    user_data = get_user_input(fields)
    if st.button("Process Data"):
        required_fields = process_data(user_data, fields)

        display_required_fields_warnings(required_fields)
        if not required_fields:
            with st.spinner("Processing data..."):
                response = requests.post(
                    "http://localhost:5000/predict", data=user_data
                )
                if response.text:
                    st.success("Data processed successfully!")
                    st.text(f"Response from server: {response.text}")

                    expander = st.expander("Additional Information", expanded=False)
                    with expander:
                        display_additional_info()
                else:
                    st.error("Failed to process data. Please try again.")
                    st.text(f"Response from server: {response.text}")


if __name__ == "__main__":
    main()
