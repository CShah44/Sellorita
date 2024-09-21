import streamlit as st
import streamlit_shadcn_ui as ui
from io import BytesIO
from PIL import Image
from ContentGen.text_to_ad_image import get_image
from ContentGen.image_to_video import generate_video_ad

# Page title
st.title("Sellorita AdMaker AI")

# Create a card for the Ad Creation Form
with ui.card(key="card1"):
    st.subheader("Ad Creation Form")

    # Input fields with placeholders
    product_name_input = ui.input("Product Name", placeholder="Enter product name")
    product_description_input = ui.input("Product Description", placeholder="Enter product description")
    brand_name_input = ui.input("Brand Name", placeholder="Enter brand name")
    about_brand_input = ui.input("About Brand", placeholder="Tell us about your brand")
    
    # Dropdown selections
    st.subheader("Type of Ad")
    type_ad = ['Social Media', 'Billboard', 'Print', 'Sale Offer']
    selected_ad_type_input = st.selectbox("Select an option", type_ad, key="1")

    st.subheader("Target Audience")
    target_audience = ['Kids', 'Teens', 'Adults', 'All']
    selected_audience_input = st.selectbox("Select your audience", target_audience, key="2")

    # Form submit button
    submit_button = st.button("Generate Ad")

# Only assign values when the form is submitted
if submit_button:
    # Capture values from form inputs
    product_name = product_name_input
    product_description = product_description_input
    brand_name = brand_name_input
    brand_info = about_brand_input
    selected_ad_type = selected_ad_type_input
    selected_audience = selected_audience_input

    ui.success("Ad creation in progress...")

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
    ui.image(image, caption="Generated Ad Image", use_column_width=True)

    # Convert image to video ad
    try:
        video = generate_video_ad(image)
        ui.video(video)
    except Exception as e:
        ui.error(f"Error generating video: {e}")
        video = None

    # Convert the image for download
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)  # Reset buffer pointer

    # Download button for the generated ad image
    ui.download_button(
        label="Download Ad Image",
        data=buffer,
        file_name="ad_image.png",
        mime="image/png"
    )
