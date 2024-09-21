import streamlit as st
from streamlit_option_menu import option_menu


# Set page configuration
st.set_page_config(page_title="Sellorita - Your AI Marketing Assistant", page_icon="💡", layout="wide")

# Background image for the app
page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
background-image: url("https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwxMTc3M3wwfDF8c2VhcmNofDF8fGZhbGx8ZW58MHx8fHwxNjIwOTY0MTQ1&ixlib=rb-1.2.1&q=80&w=1080
");
background-size: cover;
background-position: center;
}

[data-testid="stHeader"]{
background: rgba(0,0,0,0);
}

[data-testid="stToolbar"]{
right: 2rem;
}

[data-testid="stSidebar"] > div:first-child{
background-image: url("https://www.vezadigital.com/wp-content/uploads/2021/08/Sellorita-AI.png");
background-size: cover;
background-position: center;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Title and introduction
st.title("Welcome to Sellorita AI 💡")
st.markdown("""
### Your Personal Marketing Powerhouse 🚀
**Sellorita** is an advanced AI-driven assistant designed to streamline your marketing efforts. Whether you need creative ad campaigns or targeted marketing strategies, Sellorita is here to generate data-driven solutions that help you stand out in today's competitive marketplace.

With Sellorita, you can:
- **Generate powerful ad campaigns** tailored to your products in a matter of minutes.
- **Get personalized marketing strategies** that align with your brand’s vision and audience.
- **Streamline your marketing workflow** with one AI-powered assistant.

---

### What’s in Store?
- **Page 1: AdMaker**  
Create stunning, ready-to-use advertisements by simply inputting product details. Sellorita uses cutting-edge AI algorithms to generate ad images that perfectly fit your selected platform and audience.

- **Page 2: Marketing Chatbot**  
Need help fine-tuning your marketing strategies? Sellorita's chatbot will assist you in generating comprehensive marketing plans, ideas for campaigns, and expert advice—all customized to your brand and goals.

Jump in and explore Sellorita’s full potential to elevate your marketing efforts!
""")

# Sidebar menu for navigation
# selected = option_menu(
#     menu_title=None,
#     options=["Home", "AdMaker", "Marketing Chatbot"],
#     icons=["house", "image", "chat-dots"],
#     menu_icon="cast",
#     default_index=0,
#     orientation="horizontal"``
# )

# if selected == "AdMaker":
    


    
# elif selected == "Marketing Chatbot":
#     st.write("Welcome to the Marketing Chatbot page.")
#     # Marketing Chatbot functionality here
