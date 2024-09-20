import streamlit as st
from io import BytesIO
from PIL import Image
from AdGen.text_to_ad_image import get_image

# Define the form
with st.form("Form"):
    st.write("Please fill the form")
    
    # Input fields
    product_name_input = st.text_input('Product Name')
    product_description_input = st.text_input('Product Description')
    brand_name_input = st.text_input('Brand Name')
    about_brand_input = st.text_input('About Brand')
    
    # Dropdown selections
    st.subheader("Type of ad:")
    type_ad = ['Social Media', 'Billboard', 'Print', 'Sale Offer']
    selected_ad_type_input = st.selectbox("Select an option:", type_ad, key="1")

    st.subheader("Target Audience:")
    target_audience = ['Kids', 'Teens', 'Adults', 'All']
    selected_audience_input = st.selectbox("Select an option:", target_audience, key="2")

    # Submit button for form
    submit_button = st.form_submit_button(label="Submit")

# Only assign values when the form is submitted
if submit_button:
    # Assign values to variables after form submission
    product_name = product_name_input
    product_description = product_description_input
    brand_name = brand_name_input
    brand_info = about_brand_input
    selected_ad_type = selected_ad_type_input
    selected_audience = selected_audience_input
    
    st.write("Form submitted!")

    brand_details = {
        "brand_name": brand_name,
        "about_brand": brand_info
    }

    product_details = {
        "product_name": product_name,
        "product_description": product_description
    }

    image = get_image(brand_details, product_details, type_of_ad = selected_ad_type, target_audience = selected_audience)
    st.image(image, caption="Generated Ad Image")
    
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)  # Reset the pointer to the beginning of the buffer

    # Create a download button
    st.download_button(
        label="Download Image",
        data=buffer,
        file_name="your_ad.png",
        mime="image/png"
    )