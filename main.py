import streamlit as st

with st.form("form"):
    st.write("Please fill the form")
    product_name=st.text_input('Product_name')
    product_description=st.text_input('Product_description')
    brand_name=st.text_input('Brand_name')
    brand_vision=st.text_input('Brand_description')
    user_description=st.text_input('Describe how you want your ad to be')
# type_of_ad is like "social media campaign" or "billboard" or "print" or "sale offer"
    options=['social media','billboard','print','sale offer']
