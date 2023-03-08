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
    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
    if uploaded_file is not None:
        # Save the filename in a variable
        filename = uploaded_file.name
        return uploaded_file
    else:
        return None


# Define the Streamlit app
def main():
    # Set the app header and sidebar
    st.set_page_config(page_title='Oivié-E', page_icon=':bar_chart:', layout='wide')
    st.sidebar.title('Oivié-E')
    st.sidebar.subheader('Your Instant Text-to-Insights Tool')
    st.sidebar.markdown('With Oivié-E, you can become a data analyst in just a few minutes!')
    st.sidebar.markdown('Just upload your CSV file and ask your question about the data -- any question you want!')
    st.sidebar.markdown(' ')

    # Allow the user to upload a CSV file
    st.sidebar.markdown('### Upload a CSV file')
    filename = upload_file()
    filename_suc = False
    if filename:
        filename_suc = True

    # Ask the user to specify an OpenAI API key
    st.sidebar.markdown('### Enter your OpenAI API key')
    api_key = st.sidebar.text_input("", type="password")
    api_key_suc = False
    if api_key:
        openai.api_key = api_key
        os.environ['OPENAI_API_KEY'] = api_key
        st.sidebar.success("API key set successfully!")
        api_key_suc = True

    # Allow the user to interact with the CSV data through a chatbot
    if filename_suc and api_key_suc:
        st.title('CHAT with your CSV')
        st.markdown('Type a question that you want to know about the data! e.g : how many rows in the file?')
        st.markdown('You can ask as many questions as you want; the sky is the limit (and the 200MB limit).')
        user_input = st.text_input('', key='input', height=50)

        if st.button('Send', key='send', height=50):
            # Use the chatbot to process the user's input
            agent = create_csv_agent(OpenAI(temperature=0), filename, verbose=True)
            results_st = agent.run(user_input)
            response = results_st
            # Display the chatbot's response in a text area
            st.text_area('ChatBot:', value=str(response), key='output', height=200)


if __name__ == "__main__":
    main()
