import os
import html
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import streamlit as st
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from AdGen.text_to_ad_image import get_image

# Function to sanitize the response
def sanitize_response(response):
    # Escape HTML
    response = html.escape(response)
    # Additional content filtering can be added here
    return response

# Load API key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Initialize the language model
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)

#################################################################################################################################################

# Define a prompt template for generating ad descriptions
prompt_template_for_ad = PromptTemplate.from_template("You are an expert ad designer for an elite marketing company, that helps users market their product. So based on the query that you get, make a brief prompt for an image generation model, not specifying any technical stuff about the image, telling the important aspects about the product that must be shown in the ad. Even if the query given is a one word description, think of some important and highlighting features of that, and create the prompt: {req}")

# Create a chain for generating ad descriptions
chain_for_ad_gen = LLMChain(
    llm=llm,
    prompt=prompt_template_for_ad
)

# Function to generate an ad image from the user's query
def make_add_from_req(req):
    try:
        # Generate an ad description using the language model
        ad_description = chain_for_ad_gen.run(req)
        # Generate an image based on the ad description
        # gen_image = get_image(ad_description)
        print(ad_description)
        return ad_description
    except Exception as e:
        print(f"Error handled: {e}")
        return "An error occurred while generating the ad. Please try again."

# Define the tool
ad_gen_tool = Tool(
    name="AdGenerator",
    func=make_add_from_req,
    description="Generates the desired ad from the given description"
)

# Create the agent
agent = initialize_agent(
    tools=[ad_gen_tool],
    llm=llm,
    agent_type=AgentType.REACT_DOCSTORE,
    handle_parsing_errors = True
)

##########################################################################################################

# Define a prompt template
prompt_template = PromptTemplate.from_template("You are a marketing assistant. Your primary task is to suggest users marketing strategies to promote their product better, but you will also look at what the user is asking you, and will help him with that: {query}")

# Create a chain
chain = LLMChain(
    llm=llm,
    prompt=prompt_template
)

# Streamlit app
st.title("AI Marketing Assistant")

query = st.text_input("Enter your query:")

if st.button("Submit"):
    response = agent.run(query)
    
    # Create a placeholder for the typewriting effect
    placeholder = st.empty()
    
    # Stream the response with a typewriting effect
    full_response = ""
    for chunk in response:
        sanitized_chunk = sanitize_response(chunk)
        full_response += sanitized_chunk
        placeholder.markdown(full_response, unsafe_allow_html=True)