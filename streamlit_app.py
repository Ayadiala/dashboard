
import pandas as pd
import streamlit as st
import subprocess
import os
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
import openai


# Create a function to upload the CSV file
def upload_file():
    uploaded_file = st.file_uploader("Choose a file", type=['csv'])
    if uploaded_file is not None:
        # Save the filename in a variable
        filename = uploaded_file.name
        return filename
    else:
        return None

# Create the Streamlit app
def main():
    # Ask the user to specify a variable
    # Define the OpenAI API key input field in the sidebar
    api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")

    # Initialize the OpenAI API with the user's inputted API key
    if api_key:
       openai.api_key = api_key
       os.environ['OPENAI_API_KEY'] = api_key
       st.write("API key set successfully!")
    # Display the variable name
    st.title("Upload CSV file")
    filename = upload_file()
    if filename is not None:
        st.write("File uploaded: ", filename)
    # Set the app header
    agent = create_csv_agent(OpenAI(temperature=0), filename, verbose=True)

    st.title('ChatBot')
    st.write('Type a message to get started!')
    user_input = st.text_input('You:', key='input')
    results_st=agent.run("user_input")

    if st.button('Send', key='send'):
        # Get the chatbot's response
        response = results_st

        # Display the chatbot's response in a text area
        st.text_area('ChatBot:', value=str(response), key='output', height=200)


if __name__ == "__main__":
    main()
