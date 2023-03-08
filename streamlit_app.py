import pandas as pd
import streamlit as st
import subprocess
import os
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
import openai


# Define some style elements for the app
SIDEBAR_WIDTH = 300
COLORS = {
    'primary': '#2f4f4f',
    'secondary': '#708090',
    'background': '#f5f5f5',
    'text': '#222222',
}



# Function to upload a CSV file
def upload_file():
    uploaded_file = st.file_uploader("Choose a file", type=['csv'])
    if uploaded_file is not None:
        # Save the filename in a variable
        filename = uploaded_file.name
        return uploaded_file
    else:
        return None


# Define the Streamlit app
def main():
    # Ask the user to specify an OpenAI API key
    st.set_page_config(page_title='Inisght-E', page_icon=':bar_chart:', layout='wide')
    st.title("Inisght-E: Your Instant Text-to-Insights Tool")
    st.title("Get data-driven insights like never before!")
    st.write("With Inisght-E, you don't need to spend months learning complex analytical software. You can become a data analyst in just a few minutes! ")
    st.write("Just load your CSV and ask your question about the data, any question you want! ")
    api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")

    # Allow the user to upload a CSV file
    filename = upload_file()
    filename_suc = False
    if filename:
        filename_suc = True

    # Initialize the OpenAI API with the user's inputted API key
    api_key_suc = False
    if api_key:
        openai.api_key = api_key
        os.environ['OPENAI_API_KEY'] = api_key
        st.write("API key set successfully!")
        api_key_suc = True

    # Allow the user to interact with the CSV data through a chatbot
    if filename_suc and api_key_suc:
        st.title('Success ! CHAT with the CSV')
        st.write('Type a question that you want to know about the data! e.g : how many rows in the file? ')
        st.write('You can ask as many questions as you want; the sky is the limit (and the 200MB limit) ')
        user_input = st.text_input('You:', key='input')

        if st.button('Send', key='send'):
            # Use the chatbot to process the user's input
            agent = create_csv_agent(OpenAI(temperature=0), filename, verbose=True)
            results_st = agent.run(user_input)
            response = results_st
            # Display the chatbot's response in a text area
            st.text_area('ChatBot:', value=str(response), key='output', height=200)


if __name__ == "__main__":
    main()
