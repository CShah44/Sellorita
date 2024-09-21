import os
import html
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, trim_messages
from operator import itemgetter
from langchain_core.runnables import RunnablePassthrough


# Load API key from .env file
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
langchain_api_key = os.getenv("LANGSMITH_API_KEY")

# Initialize the language model
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=gemini_api_key)
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


# with_message_history = RunnableWithMessageHistory(llm, get_session_history)

# response = with_message_history.invoke(
#     [HumanMessage(content="Hi! I'm Bob")],
#     config=config,
# )
# # print(response.content)


chatbot_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Answer all questions to the best of your ability.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)
