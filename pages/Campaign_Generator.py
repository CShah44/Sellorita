import streamlit as st
from ContentGen.campaign_generator import generate_campaign
from io import BytesIO

st.title("Campaign Generator")

# Initialize session state to persist images, captions, and buffers across interactions
if 'images' not in st.session_state:
    st.session_state.images = []
if 'captions' not in st.session_state:
    st.session_state.captions = []
if 'buffers' not in st.session_state:
    st.session_state.buffers = []

with st.form("campaign_form"):
    brand_name = st.text_input("Brand Name")
    brand_description = st.text_area("Brand Description")
    product = st.text_input("Product Name")
    product_description = st.text_area("Product Description")
    target_audience = st.selectbox("Target Audience", ["Kids", "Teens", "Adults", "All"])
    num_posts = st.slider("Number of Social Media Posts", min_value=1, max_value=4, value=1)
    additional_design_details = st.text_area("Additional Design Details (Optional)")

    submit_button = st.form_submit_button("Generate Campaign")

if submit_button:
    with st.spinner("Please wait while we generate your campaign! This may take a few minutes."):

        # Create a data dictionary with the form data
        data = {
            "brand_name": brand_name,
            "brand_description": brand_description,
            "product_name": product,
            "product_description": product_description,
            "target_audience": target_audience,
            "no_of_posts": num_posts,
            "additional_design_details": additional_design_details
        }

        # Call the generate_campaign function with the data
        try:
            images, captions = generate_campaign(data)  # Assuming images are returned as PIL Image objects
        except Exception as e:
            st.error(f"An error occurred, please try again it'll work! ;(")
            st.stop()

        # Store images and captions in session state
        st.session_state.images = images
        st.session_state.captions = captions

        # Generate a buffer for each image
        st.session_state.buffers = []
        for image in images:
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)  # Ensure buffer pointer is at the start
            st.session_state.buffers.append(buffer)

# Display images with download buttons if images are available
if st.session_state.images:
    for idx, (image, buffer) in enumerate(zip(st.session_state.images, st.session_state.buffers)):
        # Display image
        st.image(image, caption=st.session_state.captions[idx])

        # Download button for each image with its own buffer
        st.download_button(
            label=f"Download Ad Image {idx + 1}",
            data=buffer,
            file_name=f"ad_image_{idx + 1}.png",
            mime="image/png",
            key=f"download_button_{idx}"
        )
