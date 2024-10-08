import base64
import dotenv
import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from ContentGen.text_to_ad_image import get_image_from_prompt
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from typing import List
import time
import re
import warnings
from io import BytesIO

# Ignore specific warning types
warnings.filterwarnings("ignore", message="Key 'title' is not supported in schema, ignoring", category=UserWarning)


# Chat interface
st.markdown("# AI Marketing Assistant")

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

my_img_urls = []
response_in_chat_history = []
campaign_image_urls = []
dotenv.load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7, api_key=api_key)


@tool
def make_ad_from_req(request: str) -> str:
    """Generate an image for an ad based on the given request. Always use this tool when asked to create or generate an image or an ad."""
    prompt = ChatPromptTemplate.from_template(
        "You are a top-tier ad designer at a leading marketing firm. Your task is to craft a concise and compelling prompt for an image generation model, so that it generates an ad for the given requirement, and display / create / generate the image.The user may say generate an ad or generate an image, but you should do this. Understand what the requirement is and focus on the key features and unique selling points of the product without mentioning technical details. Here is the product description {request}."
    )
    chain = prompt | model | StrOutputParser()
    ad_text = chain.invoke({"request": request})
    
    # Generate an image for the ad
    image_prompt = f"Create an image for an ad about: {ad_text}"
    image_url = get_image_from_prompt(image_prompt)

    my_img_urls.append(image_url)


    return image_url

@tool
def make_multiple_ads(request: str, no_of_ads: int) -> List[str]:
    """Based on the given request and the required number of ads / images, generate the images. Always use this tool only when asked to create a campaign of ads / images or when asked to generate / create multiple ads / images, and not when a single ad is needed."""
    prompt = ChatPromptTemplate.from_template(
        """
        You are a top-tier ad designer at a leading marketing firm, specializing in designing multiple compelling ads / images based on the requirement of how many the user wants. Your task is to craft {no_of_ads} concise and compelling prompts for an image generation model, and make sure the prompts are for image generation only, so that it generates / creates distinct, spectacular ads / images for the given requirement, and generates / creates the images / ads. Understand what the requirement is and focus on the key features and unique selling points of the product without mentioning technical details.

        Here is the product description: {request}. 

        Please provide {no_of_ads} unique ad prompts, each separated by '-|-|-|'.
        """
    )
    chain = prompt | model | StrOutputParser()
    ad_prompts = chain.invoke({"request": request, "no_of_ads":no_of_ads})
    
    
    # Split the prompts into a list
    ad_prompt_list = [prompt.strip() for prompt in ad_prompts.split('-|-|-|')]
    image_prompts = [[f"Create an ad for: {ad_text}"] for ad_text in  ad_prompt_list]
    response_in_chat_history.extend(ad_prompt_list)

    for ad_prompt in ad_prompt_list:
        image_prompt = f"Create an image for an ad about: {ad_prompt}"
        image_url = get_image_from_prompt(image_prompt)
        campaign_image_urls.append(image_url)

    return image_prompts

@tool
def suggest_marketing_tactics(request: str) -> str:
    """Provide about 8, but less than 10 concise, effective marketing strategies based on the given request."""
    prompt = ChatPromptTemplate.from_template(
        "You are a seasoned marketing assistant. Provide about 8, but less than 10 concise, effective marketing strategies to enhance product promotion. Be specific and to the point. Here is the user's query: {request}"
    )
    chain = prompt | model | StrOutputParser()

    response = chain.invoke({"request": request})
    return response

def get_images(ad_concepts):
    # Generate images for each ad concept
    for concept in ad_concepts:
        image_prompt = f"Create an advertisement image based on this concept: {concept}"
        image_url = get_image_from_prompt(image_prompt)
        campaign_image_urls.append(image_url)


@tool
def generate_ad_campaign(request: str, no_of_ads: int) -> List[str]:
    
    """Generate an ad campaign of social media posts images based on the given request and number of ads. This tool will always be used to generate images when asked to generate an ad campaign or when asked to generate multiple ads."""
    prompt = ChatPromptTemplate.from_template(
        """
        You are a creative marketing expert tasked with generating an ad campaign who creates visually stunning advertisement images. Create {no_of_ads} unique and compelling ad concepts based on the following product or brand information:

        {request}

        Output format:
        {no_of_ads} unique ad concepts, each separated by '---'.
        
        For each ad concept, provide:
        1. A catchy headline (max 10 words)
        2. A brief description of the visual elements (max 20 words)
        3. A short tagline or call-to-action (max 10 words)

        Always separate each ad concept with '---'.
        """
    )
    chain = prompt | model | StrOutputParser()
    campaign_response = chain.invoke({"request": request, "no_of_ads": no_of_ads})
    
    # Split the response into individual ad concepts
    ad_concepts = [concept.strip() for concept in campaign_response.split('---')]
    
    get_images(ad_concepts)

    return ad_concepts
    
    

tools=[make_ad_from_req, suggest_marketing_tactics, generate_ad_campaign]
memory = MemorySaver()

def stream_markdown(response):
    placeholder = st.empty()
    full_response = ""
    
    # Split the response into chunks, preserving newlines and spaces
    chunks = re.split(r'(\s+)', response)
    
    for chunk in chunks:
        full_response += chunk
        placeholder.markdown(full_response)
        
        # Adjust sleep time based on chunk content
        if chunk.strip():  # If chunk is not just whitespace
            time.sleep(0.05)  # Shorter delay for content
        elif '\n' in chunk:
            time.sleep(0.2)  # Longer delay for newlines
        else:
            time.sleep(0.01)

agent_executor = create_react_agent(model, tools)
def chat_response_and_flow(query):
    
    response = agent_executor.invoke(
        {"messages": [HumanMessage(content=f"{query}")]},
        stream_mode="values"
    )

    to_return = []
    for message in response["messages"]:
        if(message.type == "ai" and len(message.content) > 0 and len(message.response_metadata) > 0):
            to_return.append(message.content)
            response_in_chat_history.append(message.content)
    return to_return[0]

# Display chat chat_history from history on app rerun
for message in st.session_state.chat_history:
    if message["role"] == "image":
        with st.chat_message(message["role"], avatar="🏞️"):  # Using an emoji as avatar
            st.image(message["content"])
    elif message["role"] == "video":
        with st.chat_message(message["role"], avatar="🎥"):  # Using an emoji as avatar
            st.video(message["content"])
    elif message["role"] == "campaign":
        for imgs in message["content"]:
            with st.chat_message("image", avatar="🏞️"):
                st.image(imgs)
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Accept user input
if user_input := st.chat_input("Your input here..."):
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get response from the agent
    res = chat_response_and_flow(user_input)

    st.spinner("Cooking up a response...")

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream_markdown(res)

    # Add assistant response to chat history
    for rsp in response_in_chat_history:
        st.session_state.chat_history.append({"role": "assistant", "content": rsp})
    #this means there was an image generated
    if(len(my_img_urls) > 0):
        for img_url in my_img_urls:
            st.session_state.chat_history.append({"role": "image", "content": img_url})
            with st.chat_message("image", avatar="🏞️"):
                st.image(img_url, caption="Generated Ad Image", use_column_width=True)
                # buffer = BytesIO()
                # img_url.save(buffer, format="PNG")
                # buffer.seek(0)  # Reset buffer pointer

                # # Download button for the generated ad image
                # st.download_button(
                # label="Download Ad Image",
                # data=buffer,
                # file_name="ad_image.png",
                # mime="image/png",
                # key=img_url,
                # help="Click to download the generated ad image.",
                # )

                img_byte_arr = BytesIO()
                img_url.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()

                # Encode image to base64
                img_str = base64.b64encode(img_byte_arr).decode()

                # Create download link
                href = f'<a href="data:file/png;base64,{img_str}" download="generated_ad.png">Download Image</a>'
                
                # Display download button
                st.markdown(href, unsafe_allow_html=True)
                
    if(len(campaign_image_urls) > 0):
        st.session_state.chat_history.append({"role": "campaign", "content": campaign_image_urls})
        for img_url in campaign_image_urls:
            with st.chat_message("image", avatar="🏞️"):
                st.image(img_url, caption="Generated Ad Image", use_column_width=True)
                # buffer = BytesIO()
                # img_url.save(buffer, format="PNG")
                # buffer.seek(0)  # Reset buffer pointer

                # # Download button for the generated ad image
                # st.download_button(
                # label="Download Ad Image",
                # data=buffer,
                # file_name="ad_image.png",
                # mime="image/png",
                # key=img_url,
                # help="Click to download the generated ad image.",
                # )

                img_byte_arr = BytesIO()
                img_url.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()

                # Encode image to base64
                img_str = base64.b64encode(img_byte_arr).decode()

                # Create download link
                href = f'<a href="data:file/png;base64,{img_str}" download="generated_ad.png">Download Image</a>'
                
                # Display download button
                st.markdown(href, unsafe_allow_html=True)                
    # change this to add a video feature also in the chatbot
    # elif user_input == "addv":
    #     st.session_state.chat_history.append({"role": "video", "content": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"})
    #     with st.chat_message("video", avatar="🎥"):
    #         st.video(st.session_state.chat_history[-1]["content"])
        