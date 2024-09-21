import streamlit as st
from ContentGen.marketing_chatbot import sanitize_response, agent

query = st.text_input('AI MARKETING ASSISTANT')

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