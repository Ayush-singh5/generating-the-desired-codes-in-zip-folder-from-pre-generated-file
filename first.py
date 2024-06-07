##AIzaSyB_9Jz5Wp7Olwjqlmhr5SpOrr8gmrfQ038

import streamlit as st
import os
import google.generativeai as genai

# Ensure you have the latest version of Streamlit
# pip install --upgrade streamlit

st.title("Gemini Bot")

# Set the API key for Google Generative AI
api_key = "AIzaSyB_9Jz5Wp7Olwjqlmhr5SpOrr8gmrfQ038"  # Replace with your actual API key
os.environ['GOOGLE_API_KEY'] = api_key
genai.configure(api_key=api_key)

# Select the model
model = genai.GenerativeModel('gemini-pro')

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ask me anything about generating code or applications!"
        }
    ]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Process and store Query and Response
def llm_function(query):
    response = model.generate_content(query)

    # Displaying the Assistant Message
    with st.chat_message("assistant"):
        st.markdown(response.text)

    # Storing the User Message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    # Storing the Assistant Message
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response.text
        }
    )

    return response.text

# Accept user input
query = st.chat_input("What do you want to build?")

# Calling the Function when Input is Provided
if query:
    # Displaying the User Message
    with st.chat_message("user"):
        st.markdown(query)

    response_text = llm_function(query)

    # Save the response to a file in the current working directory
    if response_text:
        file_name = "generated_output.txt"
        with open(file_name, "w") as f:
            f.write(response_text)

        st.success(f"The generated output has been saved as '{file_name}' in the current directory.")
        st.write(f"Saved file: {file_name}")

        # Optionally, offer a download button for the file
        with open(file_name, "rb") as f:
            st.download_button(
                label="Download the generated output file",
                data=f,
                file_name=file_name,
                mime="text/plain"
            )
    else:
        st.error("Failed to generate a response. Please ensure the query is correctly formatted.")
