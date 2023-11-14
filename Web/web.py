import streamlit as st


def input_and_process():
    st.title("Pet Find Adoption")

    fields = {
        "Image": "file",
        "Type": "text",
        "Name": "text",
        "Age": "text",
        "Breed1": "text",
        "Breed2": "text",
        "Color1": "text",
        "Color2": "text",
        "Color3": "text",
        "MaturitySize": "text",
        "FurLength": "text",
        "Vaccinated": "text",
        "Dewormed": "text",
        "Sterilized": "text",
        "Health": "text",
        "Quantity": "text",
        "Fee": "text",
        "Description": "text",
        "AdoptionSpeed": "text",
    }

    data = {}

    for field, data_type in fields.items():
        if data_type == "file":
            data[field] = st.file_uploader(
                f"Choose {field.lower()}", type=["jpg", "jpeg", "png"]
            )
        elif data_type == "text":
            data[field] = st.text_input(f"Enter {field}*", "")

        elif data_type == "number":
            data[field] = st.number_input(f"Enter {field}", value=0)

    if st.button("Process Data"):
        if (
            fields["Image"] in data
            and data["Image"] is None
            or not all(data[field] for field in fields if field != "Image")
        ):
            st.warning("Please fill in all fields and upload an image. * is mandatory")
        else:
            st.title("Processed Data")
            if "Image" in data:
                st.image(data["Image"], caption="Uploaded Image", use_column_width=True)
            for field in fields:
                if field != "Image":
                    st.write(f"{field}: {data[field]}")

            with st.spinner("Processing data..."):
                st.success("Data processed successfully!")


def main():
    input_and_process()


if __name__ == "__main__":
    main()
