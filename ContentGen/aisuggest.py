import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import streamlit as st
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool, DuckDuckGoSearchResults

def make_prompt_for_ad_gen(req):
    return "generate an ad for: " + req

ad_gen_tool = Tool(
    name="AdGenerator",
    func = make_prompt_for_ad_gen,
    description="Generates the prompt to generate an ad for the product"
)

search_tool = DuckDuckGoSearchResults()

# Load API key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Initialize the language model
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)

# Create the agent
agent = initialize_agent(
    tools=[search_tool, ad_gen_tool],
    llm=llm,
    agent_type=AgentType.REACT
)

# Define a prompt template
prompt_template = PromptTemplate.from_template("You are a marketing assistant. Your primary task is to suggest users marketing strategies to promote their product better, but you will also look at what the user is asking and perform other tasks, such as triggering methods to generate the ad based on user requirements: {query}")

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
    
    for chunk in response:
        st.write_stream(chunk, end='', flush=True)