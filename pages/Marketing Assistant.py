import dotenv
import os
import uuid
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from ContentGen.text_to_ad_image import get_image_from_prompt
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from streamlit_shadcn_ui import button
import time
import re
import warnings

# Ignore specific warning types
warnings.filterwarnings("ignore", message="Key 'title' is not supported in schema, ignoring", category=UserWarning)


# Chat interface
st.markdown("# AI Marketing Assistant")

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'session_id_list' not in st.session_state:
    st.session_state.session_id_list = []
    first_session_id = str(uuid.uuid4())
    print("first session id = ", first_session_id)
    st.session_state.session_id_list.append(first_session_id)

my_img_urls = []
response_in_chat_history = []
# Add a button to create a new session_id
if button("New Session", variant="outline"):
    # Generate a new session_id not in session_id_set
    while True:
        new_session_id = str(uuid.uuid4())
        print("new_session_id = ", new_session_id)
        if new_session_id not in st.session_state.session_id_list:
            st.session_state.session_id_list.append(new_session_id)
            break
    my_img_urls.clear()
    response_in_chat_history.clear()
    
    # Force a rerun of the Streamlit app
    st.experimental_rerun()

dotenv.load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7, api_key=api_key)


@tool
def make_ad_from_req(request: str) -> str:
    """Generate an image for an ad based on the given request. Always use this tool when asked to create or generate an image or an ad."""
    prompt = ChatPromptTemplate.from_template(
        "You are a top-tier ad designer at a leading marketing firm. Your task is to craft a concise and compelling prompt for an image generation model, so that it generates an ad for the given requirement, and display the image.The user may say generate an ad or generate an image, but you should do this. Understand what the requirement is and focus on the key features and unique selling points of the product without mentioning technical details. Here is the product description {request}"
    )
    chain = prompt | model | StrOutputParser()
    ad_text = chain.invoke({"request": request})
    
    # Generate an image for the ad
    image_prompt = f"Create an image for an ad about: {ad_text}"
    image_url = get_image_from_prompt(image_prompt)

    my_img_urls.append(image_url)

    return image_url

@tool
def make_multiple_ads(request: str) -> str:
    """Based on the given request and the required number of ads / images, generate the images. Always use this tool when asked to create or generate an image or an ad."""
    prompt = ChatPromptTemplate.from_template(
        "You are a top-tier ad designer at a leading marketing firm, specializing in designing multiple compelling ads / images based on the requirement of how many the user wants. Your task is to craft multiple concise and compelling prompts for an image generation model, so that it generates distinct, spectacular ads for the given requirement, and displays the images.The user may say generate multiple ads or generate some images, but you should do this. Understand what the requirement is and focus on the key features and unique selling points of the product without mentioning technical details. Here is the product description {request}, and the number of ads they want {num_of_ads}"
    )
    chain = prompt | model | StrOutputParser()
    ad_text = chain.invoke({"request": request})
    
    # Generate an image for the ad
    image_prompt = f"Create an image for an ad about: {ad_text}"
    image_url = get_image_from_prompt(image_prompt)

    my_img_urls.append(image_url)

    return image_url

@tool
def suggest_marketing_tactics(request: str) -> str:
    """Provide about 8, but less than 10 concise, effective marketing strategies based on the given request."""
    prompt = ChatPromptTemplate.from_template(
        "You are a seasoned marketing assistant. Provide about 8, but less than 10 concise, effective marketing strategies to enhance product promotion. Be specific and to the point. Here is the user's query: {request}"
    )
    chain = prompt | model | StrOutputParser()
    response = chain.invoke({"request": request})
    return response

tools=[make_ad_from_req, suggest_marketing_tactics]
memory = MemorySaver()

agent_executor = create_react_agent(model, tools, checkpointer=memory)

# agent_executor = create_react_agent(model, tools)

print("session id = ", st.session_state.session_id_list[-1])
config = {"configurable": {"thread_id": f"{st.session_state.session_id_list[-1]}"}}

# response1 = agent_executor.invoke(
#     {"messages": [HumanMessage(content="Hi, I'm Bob!")]}, config1
# )

# for message in response1:
#     print(message.content)

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

def chat_response_and_flow(query):
    # Get the chat history
    recent_history = st.session_state.chat_history[-5:]
  
    chat_history = [HumanMessage(content=m["content"]) if m["role"] == "user" else AIMessage(content=m["content"]) 
                    for m in recent_history if m["role"] in ["user", "assistant"]]
    
    # Add the new query
    chat_history.append(HumanMessage(content=query))
    
    response = agent_executor.invoke(
        {"messages": chat_history},
        config=config,
        stream_mode="values"
    )

    to_return = []
    for message in response["messages"]:
        if(message.type == "ai" and len(message.content) > 0 and len(message.response_metadata) > 0):
            to_return.append(message.content)
            response_in_chat_history.append(message.content)
    print(to_return[0])
    return to_return[0]

# Display chat chat_history from history on app rerun
for message in st.session_state.chat_history:
    if message["role"] == "image":
        with st.chat_message(message["role"], avatar="🏞️"):  # Using an emoji as avatar
            st.image(message["content"])
    elif message["role"] == "video":
        with st.chat_message(message["role"], avatar="🎥"):  # Using an emoji as avatar
            st.video(message["content"])
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

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream_markdown(res)


    # Add assistant response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": response_in_chat_history[0]})
    #this means there was an image generated
    if(len(my_img_urls) > 0):
        for img_url in my_img_urls:
            st.session_state.chat_history.append({"role": "image", "content": img_url})
            with st.chat_message("image", avatar="🏞️"):
                st.image(img_url, caption="Generated Ad Image", use_column_width=True)

    # change this to add a video feature also in the chatbot
    # elif user_input == "addv":
    #     st.session_state.chat_history.append({"role": "video", "content": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"})
    #     with st.chat_message("video", avatar="🎥"):
    #         st.video(st.session_state.chat_history[-1]["content"])
        