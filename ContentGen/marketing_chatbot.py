import os
import html
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import streamlit as st
from langchain.agents import AgentType, AgentExecutor, initialize_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import Tool
from .text_to_ad_image import get_image_from_prompt
from langchain_core.messages import HumanMessage, AIMessage
from langchain.memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory


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
suggest_prompt_template_for_ad = PromptTemplate.from_template("You are a top-tier ad designer at a leading marketing firm. Your task is to craft a concise and compelling prompt for an image generation model, so that it generates an ad for the given requirement. Understand what the requirement is and focus on the key features and unique selling points of the product without mentioning technical details. Here is the product description: {req}"
)

# Create a chain for generating ad descriptions
chain_for_ad_gen = LLMChain(
    llm=llm,
    prompt=suggest_prompt_template_for_ad
)

# Define a prompt template
suggest_prompt_template = PromptTemplate.from_template("You are a seasoned marketing assistant. Your main role is to provide users with effective marketing strategies to enhance their product promotion. Additionally, address any specific queries they have. Here is the user's query: {query}"
)

# Create a chain
suggestion_chain = LLMChain(
    llm=llm,
    prompt=suggest_prompt_template
)


# Function to generate an ad image from the user's query
def make_add_from_req(req):
    try:
        # Generate an ad description using the language model
        ad_description = chain_for_ad_gen.run(req)
        # Generate an image based on the ad description
        print(ad_description)
        gen_image = get_image_from_prompt(ad_description)
        st.image(gen_image, caption="Generated Ad Image")
        return gen_image
    except Exception as e:
        print(f"Error handled: {e}")
        return "An error occurred while generating the ad. Please try again."

# Define the tool
ad_gen_tool = Tool(
    name="AdGenerator",
    func=make_add_from_req,
    description="Generates the desired ad from the given input"
)

def suggest_market_strategies(req):
    try:
        # Generate an ad description using the language model
        market_tactic = suggestion_chain.run(req)
        # Generate an image based on the ad description
        print(market_tactic)
        return market_tactic
    except Exception as e:
        print(f"Error handled: {e}")
        return "An error occurred while generating the ad. Please try again."

market_tactic_tool = Tool(
    name="SuggestTactics",
    func=suggest_market_strategies,
    description="Suggests users some effective and trendy market strategies to promote their product better"
)

tools_list = [ad_gen_tool, market_tactic_tool]

##########################################################################################################
chatbot_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an advanced marketing assistant. The user may give a good description of their product or just the product that they are trying to sell. Your roles are to suggest marketing strategies so that the user can promote their product better, or to work with other tools to help them get ads for their product. You must understand what the user wants, if you don't get it, ask them for a better context, like if they want suggestions for market tactics or want to get an ad generated",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# Create the agent
agent = initialize_agent(
    llm=llm,
    tools=tools_list,
    agent_type=AgentType.REACT_DOCSTORE,
    handle_parsing_errors=True,
    prompt = chatbot_prompt
)

demo_ephemeral_chat_history_for_chain = ChatMessageHistory()

agent_executor = AgentExecutor(agent=agent, tools=tools_list, verbose=True)

conversational_agent_executor = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: demo_ephemeral_chat_history_for_chain,
    input_messages_key="input",
    output_messages_key="output",
    history_messages_key="chat_history",
)

################################################################################################################################################3

# Streamlit app
st.title("AI Marketing Assistant")

query = st.text_input("Enter your query:")

if st.button("Submit Query"):
    response = agent.run(query)
    
    # Create a placeholder for the typewriting effect
    placeholder = st.empty()
    
    # Stream the response with a typewriting effect
    full_response = ""
    for chunk in response:
        sanitized_chunk = sanitize_response(chunk)
        full_response += sanitized_chunk
        placeholder.markdown(full_response, unsafe_allow_html=True)