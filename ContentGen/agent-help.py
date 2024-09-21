from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import initialize_agent, AgentExecutor
from langchain_core.messages import HumanMessage, AIMessage
import os
from langchain.tools import Tool

api_key = os.getenv("GEMINI_API_KEY")

model = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)


prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a friendly assistant called Max."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

def tool1(req):
    return f"Response + {req}"
    
# Define the tool
tool_made1 = Tool(
    name="Tool-1",
    func=tool1,
    description="Gives the output"
)
tools = [tool_made1]

agent = initialize_agent(
    llm=model,
    prompt=prompt,
    tools=tools
)

agentExecutor = AgentExecutor(
    agent=agent,
    tools=tools
)

def process_chat(agentExecutor, user_input, chat_history):
    response = agentExecutor.invoke({
        "input": user_input,
        "chat_history": chat_history
    })
    return response["output"]

if __name__ == '__main__':
    chat_history = []

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break

        response = process_chat(agentExecutor, user_input, chat_history)
        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=response))

        print("Assistant:", response)