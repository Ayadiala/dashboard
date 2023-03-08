
import pandas as pd
import streamlit as st
import subprocess

# Define the list of dependencies and their versions
requirements = [
    "openai",
    "langchain",
]

# Install the dependencies using pip
for requirement in requirements:
    subprocess.check_call(["pip", "install", requirement])

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
    st.title("Upload CSV file")
    filename = upload_file()
    if filename is not None:
        st.write("File uploaded: ", filename)

if __name__ == "__main__":
    main()
