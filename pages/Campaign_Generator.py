import streamlit as st
from ContentGen.campaign_generator import generate_campaign
from io import BytesIO

st.title("Campaign Generator")

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
    st.success("Please wait while we generate your campaign! This may take a few minutes.")

    # Create a data dictionary with the form data to be passed on to the generator
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
    image_urls, captions = generate_campaign(data)

    for url in image_urls:
        st.image(url, caption=captions[image_urls.index(url)])
        buffer = BytesIO()
        url.save(buffer, format="PNG")
        buffer.seek(0)  # Reset buffer pointer

                # Download button for the generated ad image
        st.download_button(
        label="Download Ad Image",
        data=buffer,
        file_name="ad_image.png",
        mime="image/png",
        key=image_urls.index(url), 
        help="Click to download the generated ad image.",
        )

