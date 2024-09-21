import streamlit as st
from streamlit_option_menu import option_menu

page_bg_img ="""
<style>
[data-testid="stAppViewContainer"]{
background-image: url("https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.vezadigital.com%2Fpost%2Ftop-5-ways-to-use-artificial-intelligence-ai-for-digital-marketing&psig=AOvVaw3ssW1_xYUKQyTASlgNqpyi&ust=1727002212226000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCIj5l-Tu04gDFQAAAAAdAAAAABAE")
background-size: cover ;
}}

[data-testid="stHeader]{{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar]{{
right: 2rem;
}}

[data-testid="stSidebar] > div:first-child{{
background-image: url("image.jpg);
background-position: center;
}}
<style>
"""
st.markdown(page_bg_img,unsafe_allow_html=True)
st.title("Sellorita!")
# Page configuration
# st.set_page_config(
#     page_title="Sellorita",
#     page_icon="💡",
#     layout="wide"
# )


