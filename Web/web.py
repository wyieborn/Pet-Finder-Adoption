import streamlit as st
import os


def input_and_process():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    img_filename = "logo.png"
    try:
        st.image(img_filename, use_column_width=True)
    except FileNotFoundError:
        st.error(
            "Image not found in the specified folder. Please provide the correct image filename."
        )

    st.title("Pet Find Adoption")

    fields = {
        "Image": {"type": "file", "required": True},
        "Type": {"type": "text", "required": True},
        "Name": {"type": "text", "required": True},
        "Age": {"type": "number", "required": True},
        "Breed1": {"type": "text", "required": False},
        "Breed2": {"type": "text", "required": False},
        "Color1": {"type": "text", "required": False},
        "Color2": {"type": "text", "required": False},
        "Color3": {"type": "text", "required": False},
        "MaturitySize": {"type": "text", "required": False},
        "FurLength": {"type": "text", "required": False},
        "Vaccinated": {"type": "text", "required": False},
        "Dewormed": {"type": "text", "required": False},
        "Sterilized": {"type": "text", "required": False},
        "Health": {"type": "text", "required": False},
        "Quantity": {"type": "number", "required": False},
        "Fee": {"type": "number", "required": False},
        "Description": {"type": "text", "required": False},
        "AdoptionSpeed": {"type": "number", "required": False},
    }

    data = {}

    for field, options in fields.items():
        field_type = options["type"]
        required = options["required"]

        if field_type == "file":
            data[field] = st.file_uploader(
                f"Choose {field.lower()}", type=["jpg", "jpeg", "png"]
            )
        elif field_type == "text":
            data[field] = st.text_input(f"Enter {field}{'*' if required else ''}", "")
        elif field_type == "number":
            data[field] = st.number_input(
                f"Enter {field}{'*' if required else ''}", value=0
            )

    if st.button("Process Data"):
        missing_required_fields = [
            field
            for field, options in fields.items()
            if options["required"] and not data.get(field)
        ]

        if missing_required_fields:
            st.warning("Please fill in all mandatory fields.")
            for field in missing_required_fields:
                st.markdown(
                    f"<span style='color:red'>Required field: {field}</span>",
                    unsafe_allow_html=True,
                )
        else:
            st.title("Processed Data")
            if "Image" in data and data["Image"] is not None:
                st.image(data["Image"], caption="Uploaded Image", use_column_width=True)
            for field in fields:
                if field != "Image":
                    st.write(f"{field}: {data[field]}")

            with st.spinner("Processing data..."):
                # Simulate processing delay
                import time

                time.sleep(3)
                st.success("Data processed successfully!")


def main():
    input_and_process()


if __name__ == "__main__":
    main()
