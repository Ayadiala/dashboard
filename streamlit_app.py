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
    api_key = st.secrets.db_credentials.password
    # Ask the user to specify an OpenAI API key
    st.set_page_config(page_title='Inisght-E', page_icon=':bar_chart:', layout='wide')
    st.title("Inisght-E: Your Instant Text-to-Insights Tool")
    st.title("Get data-driven insights like never before!")
    st.write("With Inisght-E, you don't need to spend months learning complex analytical software. You can become a data analyst in just a few minutes! ")
    st.write("Just load your CSV and ask your question about the data, any question you want! ")
    #api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")

    # Allow the user to upload a CSV file
    filename = upload_file()
    filename_suc = False
    if filename:
        filename_suc = True

    # Initialize the OpenAI API with the user's inputted API key
    if api_key:
        openai.api_key = api_key
        os.environ['OPENAI_API_KEY'] = api_key
        try:
            #st.write("sarting........!")
            openai.Completion.create(engine="davinci", prompt="Hello world", max_tokens=5)
            st.write("API key set successfully!")
            api_key_suc = True
        except openai.error.AuthenticationError:
            st.write("<b>Invalid API key. Please check your API key and try again.</b>", unsafe_allow_html=True)
            api_key_suc = False
            
    df = pd.read_csv(filename)
    df_size = True
    if df.shape[1]>25:
        st.write("<b>You have too many columns please reduce the number of columns, the maximum number of columns allowed is 24 </b>", unsafe_allow_html=True)
        df_size = False
    # Allow the user to interact with the CSV data through a chatbot
    if filename_suc and api_key_suc and df_size:
        # Define the progress message to display to the user
        progress_text = "Operation in progress. Please wait."

        # Create a progress bar object with 0% completion and the progress message
        my_bar = st.progress(0, text=progress_text)

        # Initialize the percent_complete variable to 0
        percent_complete = 0

        # Create an agent object that uses an OpenAI model and a file name
        agent = create_csv_agent(OpenAI(temperature=0), filename, verbose=True)

        # Increment the progress bar by 20% and update the progress message
        my_bar.progress(percent_complete + 20, text=progress_text)

        # Update the percent_complete variable to reflect the updated progress
        percent_complete = percent_complete + 20

        # Run the agent on a specific question and store the results in a variable
        results_st = agent.run('what are the columns name in the data?')

        # Increment the progress bar by another 20% and update the progress message
        my_bar.progress(percent_complete + 20, text=progress_text)

        # Update the percent_complete variable to reflect the updated progress
        percent_complete = percent_complete + 20

        # Create another OpenAI object using a different model name
        llm = OpenAI(model_name="gpt-3.5-turbo", n=2)

        # Increment the progress bar by another 20% and update the progress message
        my_bar.progress(percent_complete + 20, text=progress_text)

        # Update the percent_complete variable to reflect the updated progress
        percent_complete = percent_complete + 20

        # Ask a question that concatenates the previous results and store the output in a variable
        Example_results = llm("What are 5 diversified smart non-unique data analysis questions we can ask about a data with those columns; results_st "+results_st )

        # Increment the progress bar by another 20% and update the progress message
        my_bar.progress(percent_complete + 20, text=progress_text)

        # Update the percent_complete variable to reflect the updated progress
        percent_complete = percent_complete + 20

        # Increment the progress bar one last time
        my_bar.progress(percent_complete + 20, text=progress_text)

        
        st.title('Success ! You can CHAT with the CSV')
        st.write('Type a question that you want to know from the data!  <i>below some exmaples based on your data</i> ', unsafe_allow_html=True)
        st.text(Example_results)
        st.write('You can ask as many questions as you want; the sky is the limit (and the 200MB limit) ')        
        user_input = st.text_input('You:', key='input')
        if st.button('Show me the Magic!', key='send'):
            # Use the chatbot to process the user's input
            results_st = agent.run(user_input)
            response = results_st
            # Display the chatbot's response in a text area
            st.text_area('ChatBot:', value=str(response), key='output', height=200)


if __name__ == "__main__":
    main()
