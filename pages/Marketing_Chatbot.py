import streamlit as st
from ContentGen.marketing_chat_new_llm import chat_response_and_flow
import uuid

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []


# Function to display chat messages
def display_chat():
    for messages in st.session_state.chat_history:
        if messages['role'] == 'AI':
            st.markdown(f"**AI:** {messages['content']}")
        elif messages['role'] == 'Tool':
            st.image(messages['content'])
        else:
            st.markdown(f"**You:** {messages['content']}")

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
        res, img = chat_response_and_flow(user_input)
        # Add agent response to chat history

        st.session_state.chat_history.append({"role": "AI", "content": res})
        # st.session_state.chat_history.append({"role": "Tool", "content": img})
        # Display updated chat history
        display_chat()
