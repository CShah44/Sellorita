import streamlit as st
from io import BytesIO
from PIL import Image
import base64
from ContentGen.text_to_ad_image import get_image
from ContentGen.image_to_video import generate_video_ad

# Set page configuration with a new theme
st.set_page_config(page_title="Sellorita AdMaker AI", page_icon="💡", layout="wide")

# Page title with enhanced design
st.markdown('<h1 class="title">Sellorita AdMaker AI</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="subheader">Create Stunning Advertisements in Seconds</h2>', unsafe_allow_html=True)
st.markdown("---")

product_name_input= st.text_input("Product Name")

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
    with st.spinner("Ad creation in progress... Please wait!"):
        image = get_image(brand_details, product_details, type_of_ad=selected_ad_type, target_audience=selected_audience)
    
    st.image(image, caption="Generated Ad Image", use_column_width=True)

    st.success("Ad image generated successfully!")
    
    # Convert image to bytes
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    # Encode image to base64
    img_str = base64.b64encode(img_byte_arr).decode()

    # Create download link
    href = f'<a href="data:file/png;base64,{img_str}" download="generated_ad.png">Download Image</a>'
    
    # Display download button
    st.markdown(href, unsafe_allow_html=True)
    
    # Generate video ad from the image
    try:
        with st.spinner("Generating video ad... This may take a few minutes."):
            video = generate_video_ad(image)

        st.success("Video generated successfully!")

        # Store the video in session state
        st.session_state.video_buffer = BytesIO(video)

        # Display the video using the stored buffer
        st.video(st.session_state.video_buffer)

        # Encode video to base64
        video_str = base64.b64encode(video).decode()

        # Create download link for video
        video_href = f'<a href="data:video/mp4;base64,{video_str}" download="ad_video.mp4">Download Video</a>'

        # Display download button for video
        st.markdown(video_href, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error generating video. Sorry, please try again later. {e}")

        