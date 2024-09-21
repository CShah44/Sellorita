import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
import dotenv
import os
from ContentGen.text_to_ad_image import get_image_from_prompt
from langchain_core.messages import HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []


dotenv.load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7, api_key=api_key)

my_urls = []

@tool
def make_ad_from_req(request: str) -> str:
    """Generate an ad based on the given request."""
    prompt = ChatPromptTemplate.from_template(
        "You are a top-tier ad designer at a leading marketing firm. Your task is to craft a concise and compelling prompt for an image generation model, so that it generates an ad for the given requirement. Understand what the requirement is and focus on the key features and unique selling points of the product without mentioning technical details. Here is the product description {request}"
    )
    chain = prompt | model | StrOutputParser()
    ad_text = chain.invoke({"request": request})
    
    # Generate an image for the ad
    image_prompt = f"Create an image for an ad about: {ad_text}"
    image_url = get_image_from_prompt(image_prompt)
    # st.image(image_url, caption="Generated Ad Image", use_column_width=True)

    my_urls.append(image_url)

    return image_url


@tool
def suggest_marketing_tactics(request: str) -> str:
    """Provide marketing strategies based on the given request."""
    prompt = ChatPromptTemplate.from_template(
        "You are a seasoned marketing assistant. Your main role is to provide users with effective marketing strategies to enhance their product promotion. Additionally, address any specific queries they have. Here is the user's query: {request}"
    )
    chain = prompt | model | StrOutputParser()
    response = chain.invoke({"request": request})

    return response

tools=[make_ad_from_req, suggest_marketing_tactics]
# memory = MemorySaver()
# agent_executor = create_react_agent(model, tools, checkpointer=memory)

agent_executor = create_react_agent(model, tools)

# config1 = {"configurable": {"thread_id": "abc123"}}

# response1 = agent_executor.invoke(
#     {"messages": [HumanMessage(content="Hi, I'm Bob!")]}, config1
# )

# for message in response1:
#     print(message.content)

def chat_response_and_flow(query):
    response = agent_executor.invoke(
        {"messages": [HumanMessage(content=f"{query}")]},
        stream_mode="values"
    )

    to_return = []
    image_to_print = []
    for message in response["messages"]:
        if(message.type == "ai" and len(message.content) > 0 and len(message.response_metadata) > 0):
            to_return.append(message.content)
        # if(message.type == "tool"):
        #     image_to_print.append()

    return to_return[0]

# Function to display chat messages
def display_chat():
    for messages in st.session_state.chat_history:
        if messages['role'] == 'AI':
            st.markdown(f"**AI:** {messages['content']}")
        # elif messages['role'] == 'Tool':
        #     st.image(messages['content'])
        else:
            st.markdown(f"**You:** {messages['content']}")

    if(len(my_urls) > 0):
        for url in my_urls:
            st.image(url, caption="Generated Ad Image", use_column_width=True)

# Chat interface
st.title("AI Marketing Assistant")

# Display chat history
display_chat()

# User input
user_input = st.text_input("Your message:", key="input")

if st.button("Send"):
    if user_input:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "User", "content": user_input})
        
        # Get response from the agent
        res = chat_response_and_flow(user_input)
        # Add agent response to chat history

        st.session_state.chat_history.append({"role": "AI", "content": res})
        # st.session_state.chat_history.append({"role": "Tool", "content": img})
        # Display updated chat history
        display_chat()
