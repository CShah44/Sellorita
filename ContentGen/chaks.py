from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
import dotenv
import os
from text_to_ad_image import get_image_from_prompt
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
import json

dotenv.load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7, api_key=api_key)

@tool
def make_ad_from_req(request: str) -> str:
    """Generate an ad based on the given request."""
    prompt = ChatPromptTemplate.from_template(
        "You are a top-tier ad designer at a leading marketing firm. Your task is to craft a concise and compelling prompt for an image generation model, so that it generates an ad for the given requirement. Understand what the requirement is and focus on the key features and unique selling points of the product without mentioning technical details. Here is the product description {request}"
    )
    chain = prompt | model | StrOutputParser()
    ad_text = chain.invoke({"request": request})
    
    # Generate an image for the ad
    image_prompt = f"Create an image for an ad about: {request}"
    image_url = get_image_from_prompt(image_prompt)
    
    return [ad_text, image_url]


@tool
def suggest_marketing_tactics(request: str) -> str:
    """Provide marketing strategies based on the given request."""
    prompt = ChatPromptTemplate.from_template(
        "You are a seasoned marketing assistant. Your main role is to provide users with effective marketing strategies to enhance their product promotion. Additionally, address any specific queries they have. Here is the user's query: {request}"
    )
    chain = prompt | model | StrOutputParser()
    response = chain.invoke({"request": request})

    return response

# @tool
# def have_conversation(request: str) -> str:
#     """Have a conversation with the user."""
#     prompt = ChatPromptTemplate.from_template(
#         "You are a helpful assistant. Your task is to converse with the user and provide helpful responses. Here is the user's query: {request}"
#     )
#     chain = prompt | model | StrOutputParser()
#     response = chain.invoke({"request": request})

#     return response

tools=[make_ad_from_req, suggest_marketing_tactics]

agent_executor = create_react_agent(model, tools)

response = agent_executor.invoke(
    {"messages": [HumanMessage(content="ad for blue earphones")]},
    stream_mode="values"
)

updates = []

for message in response["messages"]:
    # if(message.type == "ai" and len(message.content) > 0 and len(message.response_metadata) > 0):
    #         updates.append(message.content)
    if(message.type == "tool"):
        x = json.loads(str(message.content))
        print(x)

    updates.append(message)

