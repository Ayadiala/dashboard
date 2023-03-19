import pandas as pd  # Import the pandas library for data manipulation
import streamlit as st  # Import the Streamlit library for building interactive apps
import subprocess  # Import the subprocess library for running shell commands
import os  # Import the os library for interacting with the operating system
from langchain.agents import create_pandas_dataframe_agent  # Import a function from the langchain.agents module
from langchain.llms import OpenAI  # Import the OpenAI class from the langchain.llms module
from langchain.chains.constitutional_ai.prompts import CRITIQUE_PROMPT, REVISION_PROMPT  # Import two prompts from the langchain.chains.constitutional_ai.prompts module
from langchain.chains.llm import LLMChain  # Import the LLMChain class from the langchain.chains.llm module

import openai  # Import the OpenAI library, which is not used in this code snippet




# Define some style elements for the app
SIDEBAR_WIDTH = 300
COLORS = {
    'primary': '#2f4f4f',
    'secondary': '#708090',
    'background': '#f5f5f5',
    'text': '#222222',
}

# Define a function to check the number of columns
def check_num_columns(dataframe):
    num_cols = len(dataframe.columns)
    if num_cols > 25:
        raise ValueError(f"Error: The number of columns in the file is {num_cols}. It should be less than 25.")
    else:
        st.success(f"The number of columns in the file is {num_cols}. It is less than 25.")


# Function to upload a CSV file
def upload_file():
    uploaded_file = st.file_uploader("Choose a file", type=['csv'])
    if uploaded_file is not None:
        # Save the filename in a variable
        filename = uploaded_file.name
        return uploaded_file
    else:
        return None

def parse_critique(output_string: str) -> str:
        if "Revision request:" not in output_string:
            return output_string
        output_string = output_string.split("Revision request:")[0]
        if "\n\n" in output_string:
            output_string = output_string.split("\n\n")[0]
        return output_string
    
    
def download_sample_data(url):
    response = requests.get(url)
    open("sample_data.csv", "wb").write(response.content)

# Define the Streamlit app
def main():
    api_key = st.secrets.db_credentials.password
    # Ask the user to specify an OpenAI API key
    st.set_page_config(page_title='Inisght-E', page_icon=':bar_chart:', layout='wide')
    st.title("InsightEngine: Your Instant Text-to-Insights Tool")
    st.title("Get data-driven insights like never before!")
    st.write("With InsightEngine, you don't need to spend months learning complex analytical software. You can become a data analyst in just a few minutes! ")
    st.write("Just load your CSV and ask your question about the data, any question you want! ")
    
    with st.container():
        st.write("If you don't have a dataset, you can download a sample dataset using the button below:")
        st.write("")

        sample_data_url = "https://github.com/Ayadiala/dashboard/edit/main/sample_data.csv"
        if st.button("Download Sample Dataset"):
            download_sample_data(sample_data_url)
            st.download_button("Download Sample Dataset", data="sample_data.csv", file_name="sample_data.csv")

        st.write("")

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
    
    
    # If a file is uploaded, read it as a Pandas dataframe and check the number of columns
    if filename is not None:
        try:
            df = pd.read_csv(filename)
            check_num_columns(df)
            filename_check = True
        except ValueError as e:
            st.error(str(e))
            filename_check = False
        except Exception as e:
            st.error("Unable to load file. Please check the file format and try again, it should be less than 25 columns ! ")
            filename_check = False

 
    # Allow the user to interact with the CSV data through a chatbot
    if filename_suc and api_key_suc and  filename_check:
        # Define the progress message to display to the user
        progress_text = "Operation in progress. Please wait."

        # Create a progress bar object with 0% completion and the progress message
        my_bar = st.progress(0, text=progress_text)

        # Initialize the percent_complete variable to 0
        percent_complete = 0

        # Create an agent object that uses an OpenAI model and a file name
        agent = create_pandas_dataframe_agent(OpenAI(temperature=0), df, verbose=True)

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
        st.write('Done loading the model ')        
        # Ask a question that concatenates the previous results and store the output in a variable
        Example_results = llm("What are 5 diversified smart non-unique data analysis questions we can ask about a data with those columns; results_st "+results_st )
        
        # Increment the progress bar by another 20% and update the progress message
        my_bar.progress(percent_complete + 20, text=progress_text)

        critique_chain = LLMChain(llm=llm, prompt=CRITIQUE_PROMPT)
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
            st.text_area('InsightEngine Response:', value=str(response), key='output')

            # Progress bar for the critique part
            critique_progress_text = "Critique in progress. Please wait."
            critique_bar = st.progress(0, text=critique_progress_text)
            critique_percent_complete = 0

            raw_critique = critique_chain.run(
                input_prompt=user_input,
                output_from_model=response,
                critique_request='Tell if this answer is good. and if The model potentially should only talk about ethical things.'
            )

            critique_percent_complete += 50
            critique_bar.progress(critique_percent_complete, text=critique_progress_text)

            critique = parse_critique(output_string=raw_critique).strip()

            critique_percent_complete += 50
            critique_bar.progress(critique_percent_complete, text=critique_progress_text)

            st.markdown(f"**Ethical critique about the answer:** {critique}")




if __name__ == "__main__":
    main()
