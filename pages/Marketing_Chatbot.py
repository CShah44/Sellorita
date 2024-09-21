import streamlit as st
from ContentGen.marketing_chatbot import generate_response
import uuid

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Function to display chat messages
def display_chat():
    for messages in st.session_state.chat_history:
        print(messages)
        # if messages['role'] == 'user':
        #     st.markdown(f"**You:** {messages['content']}")
        # else:
        #     st.markdown(f"**AI:** {messages['content']}")

# Chat interface
st.title("AI Marketing Assistant")

# Display chat history
display_chat()

# User input
user_input = st.text_input("Your message:", key="input")

if st.button("Send"):
    if user_input:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "human", "content": user_input})
        
        # # Get response from the agent
        # response = conversational_agent_executor.invoke(
        #     {
        #         "input": user_input,
        #     },
        #     {'configurable': {'session_id': st.session_state.session_id}}
        # )

        response = generate_response(user_input)

        # Add agent response to chat history
        st.session_state.chat_history.append({"role": "ai", "content": response})
        
        # Clear the input box
        st.session_state.user_input = ""
        
        # Display updated chat history
        display_chat()
