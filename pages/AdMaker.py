import streamlit as st
from io import BytesIO
from PIL import Image
from ContentGen.text_to_ad_image import get_image
from ContentGen.image_to_video import generate_video_ad

# Set page configuration with a new theme
st.set_page_config(page_title="Sellorita AdMaker AI", page_icon="💡", layout="wide")

# Page title with enhanced design
st.markdown('<h1 class="title">Sellorita AdMaker AI</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="subheader">Create Stunning Advertisements in Seconds</h2>', unsafe_allow_html=True)
st.markdown("---")

product_name_input= st.text_input("Prroduct Name")

product_description_input=st.text_input("Product Description")

brand_name_input=st.text_input("Brand Name")

about_brand_input=st.text_input("About brand")

# Dropdown selections for Ad type and Target audience
st.subheader("Ad Type and Target Audience")


selected_ad_type_input = st.selectbox("AD Type",["Social Media", "Billboard", "Print", "Sale Offer"] )


selected_audience_input = st.selectbox("Target Audience", ["Kids", "Teens", "Adults", "All"])

# Submit button for ad generation
st.markdown("---")
submit_button = st.button("Generate Ad", use_container_width=True)

# Actions after submit
if submit_button:
    st.success("Ad creation in progress... Please wait!")

    # Capture input values
    product_name = product_name_input
    product_description = product_description_input
    brand_name = brand_name_input
    brand_info = about_brand_input
    selected_ad_type = selected_ad_type_input
    selected_audience = selected_audience_input

    # Create brand and product dictionaries
    brand_details = {"brand_name": brand_name, "about_brand": brand_info}
    product_details = {"product_name": product_name, "product_description": product_description}

    # Generate ad image
    image = get_image(brand_details, product_details, type_of_ad=selected_ad_type, target_audience=selected_audience)
    st.image(image, caption="Generated Ad Image", use_column_width=True)

    # Generate video ad from the image
    try:
        video = generate_video_ad(image)
        st.video(video)
    except Exception as e:
        st.error(f"Error generating video: {e}")

    # Convert image to a downloadable format
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    # Download button for the image
    st.download_button(
        label="Download Ad Image",
        data=buffer,
        file_name="ad_image.png",
        mime="image/png",
        key="download_button",
        help="Click to download the generated ad image.",
    )
