import pandas as pd
import streamlit as st
import subprocess
import os
from langchain.agents import create_pandas_dataframe_agent
from langchain.llms import OpenAI
from langchain.chains.constitutional_ai.prompts import CRITIQUE_PROMPT, REVISION_PROMPT
from langchain.chains.llm import LLMChain
import openai

SIDEBAR_WIDTH = 300
COLORS = {
    'primary': '#2f4f4f',
    'secondary': '#708090',
    'background': '#f5f5f5',
    'text': '#222222',
}

def check_num_columns(dataframe):
    num_cols = len(dataframe.columns)
    if num_cols > 25:
        raise ValueError(f"Error: The number of columns in the file is {num_cols}. It should be less than 25.")
    else:
        st.success(f"The number of columns in the file is {num_cols}. It is less than 25.")

def upload_file():
    uploaded_file = st.file_uploader("Choose a file", type=['csv'])
    if uploaded_file is not None:
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

def main():
    api_key = st.secrets.db_credentials.password
    st.set_page_config(page_title='Inisght-E', page_icon=':bar_chart:', layout='wide')
    st.title("InsightEngine: Your Instant Text-to-Insights Tool")
    st.title("Get data-driven insights like never before!")
    st.write("With InsightEngine, you don't need to spend months learning complex analytical software. You can become a data analyst in just a few minutes! ")
    st.write("Just load your CSV and ask your question about the data, any question you want! ")

    filename = upload_file()
    filename_suc = False
    if filename:
        filename_suc = True

    if api_key:
        openai.api_key = api_key
        os.environ['OPENAI_API_KEY'] = api_key
        try:
            openai.Completion.create(engine="davinci", prompt="Hello world", max_tokens=5)
            st.write("API key set successfully!")
            api_key_suc = True
        except openai.error.AuthenticationError:
            st.write("<b>Invalid API key. Please check your API key and try again.</b>", unsafe_allow_html=True)
            api_key_suc = False

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

    if filename_suc and api_key_suc and filename_check:
        progress_text = "Operation in progress. Please wait."
        my_bar = st.progress(0, text=progress_text)
        percent_complete = 0
        agent = create_pandas_dataframe_agent(OpenAI(temperature=0), df, verbose=True)
        my_bar.progress(percent_complete + 20, text=progress_text)
        percent_complete = percent_complete + 20
        results_st = agent.run('what are the columns name in the data?')
        my_bar.progress(percent_complete + 20, text=progress_text)
        percent_complete = percent_complete + 20
        llm = OpenAI(model_name="gpt-3.5-turbo", n=2)
        my_bar.progress(percent_complete + 20, text=progress_text)
        percent_complete = percent_complete + 20
        Example_results = llm("What are 5 diversified smart non-unique data analysis questions we can ask about a data with those columns; results_st " + results_st)
        my_bar.progress(percent_complete + 20, text=progress_text)
        critique_chain = LLMChain(llm=llm, prompt=CRITIQUE_PROMPT)
        percent_complete = percent_complete + 20
        my_bar.progress(percent_complete + 20, text=progress_text)
        
        st.title('Success ! You can CHAT with the CSV')
        st.write('Type a question that you want to know from the data!  <i>below some examples based on your data</i> ', unsafe_allow_html=True)
        st.text(Example_results)
        st.write('You can ask as many questions as you want; the sky is the limit (and the 200MB limit) ')        
        user_input = st.text_input('You:', key='input')
        if st.button('Show me the Magic!', key='send'):
            results_st = agent.run(user_input)
            response = results_st
            st.text_area('InsightEngine Response:', value=str(response), key='output')
            
            raw_critique = critique_chain.run(
                input_prompt=user_input,
                output_from_model=response,
                critique_request='Tell if this answer is good. and if The model potentially should only talk about ethical things.')
            critique = parse_critique(
                output_string=raw_critique).strip()
            st.markdown(f"**Ethical critique about the answer:** {critique}")

if __name__ == "__main__":
    main()

