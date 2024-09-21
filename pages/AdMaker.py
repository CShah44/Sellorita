import streamlit as st
from io import BytesIO
from PIL import Image
from ContentGen.text_to_ad_image import get_image
from ContentGen.image_to_video import generate_video_ad

# Set page configuration
st.set_page_config(page_title="Sellorita AdMaker AI", page_icon="💡", layout="wide")

# Page title and description
st.title("Sellorita AdMaker AI")
st.markdown("""
    <style>
    .title {
        color: #0073e6;
    }
    .subheader {
        color: #0056b3;
    }
    </style>
""", unsafe_allow_html=True)

st.subheader("Create Stunning Advertisements")
st.markdown("---")

# Layout using columns for better organization
col1, col2 = st.columns(2)

# Column 1: Product Information
with col1:
    st.markdown("**Product Name**")
    product_name_input = st.text_input("", placeholder="Enter product name", key="product_name")

    st.markdown("**Product Description**")
    product_description_input = st.text_input("", placeholder="Enter product description", key="product_description")

    st.markdown("**Brand Name**")
    brand_name_input = st.text_input("", placeholder="Enter brand name", key="brand_name")

# Column 2: About Brand
with col2:
    st.markdown("**About Brand**")
    about_brand_input = st.text_area("", placeholder="Tell us about your brand", height=150, key="about_brand")

# Dropdown selections
st.subheader("Ad Type and Target Audience")
col3, col4 = st.columns(2)

with col3:
    st.markdown("**Type of Ad**")
    type_ad = ['Social Media', 'Billboard', 'Print', 'Sale Offer']
    selected_ad_type_input = st.selectbox("", type_ad, key="ad_type")

with col4:
    st.markdown("**Target Audience**")
    target_audience = ['Kids', 'Teens', 'Adults', 'All']
    selected_audience_input = st.selectbox("", target_audience, key="audience")

# Button to generate ad
st.markdown("---")
submit_button = st.button("Generate Ad")

# Only assign values when the button is clicked
if submit_button:
    # Capture values from form inputs
    product_name = product_name_input
    product_description = product_description_input
    brand_name = brand_name_input
    brand_info = about_brand_input
    selected_ad_type = selected_ad_type_input
    selected_audience = selected_audience_input

    st.success("Ad creation in progress...")

    # Collect brand and product details
    brand_details = {
        "brand_name": brand_name,
        "about_brand": brand_info
    }

    product_details = {
        "product_name": product_name,
        "product_description": product_description
    }

    # Generate image using ad generation function
    image, image_bytes = get_image(brand_details, product_details, type_of_ad=selected_ad_type, target_audience=selected_audience)
    
    st.image(image, caption="Generated Ad Image", use_column_width=True)

    # Convert image to video ad
    try:
        video = generate_video_ad(image)
        st.video(video)
    except Exception as e:
        st.error(f"Error generating video: {e}")

    # Convert the image for download
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)  # Reset buffer pointer

    # Download button for the generated ad image
    st.download_button(
        label="Download Ad Image",
        data=buffer,
        file_name="ad_image.png",
        mime="image/png",
        key="download_button",
        help="Click to download the generated ad image.",
        button_type="primary"
    )
