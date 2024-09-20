import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load API key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Initialize the language model
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)

# Define a prompt template
prompt_template = PromptTemplate.from_template("You are a marketing assistant. Based on the user's requirements and details of their products, you should suggest steps they should follow to promote their product better. Suggest them market tactics to advertise their product well. Below are the details of their product: {query}")

# Create a chain
chain = LLMChain(
    llm=llm,
    prompt=prompt_template
)

# Example usage
query = "We are launching a new innovative bottle that comes with loads of features. It has a newly designed body for enhanced thermal control, and has smart features like modifying the temperature of the water, analysing contents of the liquid in the bottle, and a built in stir feature. Help me advertise this"
response = chain.run(query)
print(response)
