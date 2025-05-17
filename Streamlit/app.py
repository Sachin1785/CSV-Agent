import streamlit as st
import pandas as pd
import os
from langchain.agents import initialize_agent
from langchain.agents.agent_types import AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from streamlit_Csv import CSVHandler, parse_kv_string
import Streamlit_Tools as tools_module
from Streamlit_Tools import SYSTEM_PROMPT

st.set_page_config(page_title="CSV Agent", page_icon="📊", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

temp_dir = os.path.join(os.getcwd(), "temp")
os.makedirs(temp_dir, exist_ok=True)
temp_csv_path = os.path.join(temp_dir, "working_csv.csv")
empty_df = pd.DataFrame()

if "csv_handler" not in st.session_state:
    st.session_state.csv_handler = CSVHandler(temp_csv_path)
    st.session_state.csv_handler.df = empty_df

if "last_processed_file_id" not in st.session_state:
    st.session_state.last_processed_file_id = None

def create_agent_tools():
    st.session_state.csv_handler._load_csv()
    tools = tools_module.create_tools(st.session_state.csv_handler)
    return tools

def create_agent():
    if not st.session_state.csv_handler.df.empty and st.session_state.api_key:
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=st.session_state.api_key)
        agent_tools = create_agent_tools()
        agent = initialize_agent(tools=agent_tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True,
            agent_kwargs={"system_message": SYSTEM_PROMPT})
        return agent
    return None

with st.sidebar:
    st.title("CSV Agent")
    api_key = st.text_input("Enter Gemini API Key:", value=st.session_state.api_key, type="password")
    st.session_state.api_key = api_key
    uploaded_file_widget = st.file_uploader("Upload CSV file", type="csv", key="csv_uploader_widget") 
    csv_display = st.empty()
    status_message = st.empty()

    process_new_upload = False
    if uploaded_file_widget is not None:
        if uploaded_file_widget.file_id != st.session_state.last_processed_file_id:
            process_new_upload = True
    
    if process_new_upload:
        if os.path.exists(temp_csv_path):
            try:
                os.remove(temp_csv_path)
            except Exception:
                pass
        
        df_upload = pd.read_csv(uploaded_file_widget)
        st.session_state.csv_handler.df = df_upload
        st.session_state.csv_handler.save()
        st.session_state.last_processed_file_id = uploaded_file_widget.file_id

    if os.path.exists(temp_csv_path):
        st.session_state.csv_handler._load_csv() 
    else:
        st.session_state.csv_handler.df = pd.DataFrame()
        st.session_state.last_processed_file_id = None 

    with csv_display.container():
        st.subheader("Current CSV Data")
        if not st.session_state.csv_handler.df.empty:
            st.dataframe(st.session_state.csv_handler.df)
        else:
            st.write("Please upload a CSV file.")

    if not st.session_state.csv_handler.df.empty and st.session_state.api_key:
        status_message.success("CSV loaded and agent ready!")
    elif st.session_state.csv_handler.df.empty and not st.session_state.api_key:
        status_message.warning("Please upload a CSV file and enter your Gemini API Key")
    elif st.session_state.csv_handler.df.empty:
        status_message.warning("Please upload a CSV file")
    elif not st.session_state.api_key:
        status_message.warning("Please enter your Gemini API Key")

st.title("CSV Agent")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("How can I help with your CSV?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    if st.session_state.csv_handler.df.empty or not st.session_state.api_key:
        with st.chat_message("assistant"):
            if st.session_state.csv_handler.df.empty and not st.session_state.api_key:
                response = "Please upload a CSV file and enter your Gemini API Key."
            elif st.session_state.csv_handler.df.empty:
                response = "Please upload a CSV file first."
            elif not st.session_state.api_key:
                response = "Please enter your Gemini API Key."
            else:
                response = "Agent is not ready. Please check your inputs."
            st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
    else:
        st.session_state.csv_handler._load_csv()
        agent = create_agent()
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    st.session_state.csv_handler._load_csv()
                    response = agent.run(prompt)
                    st.write(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.session_state.csv_handler.save()
                    st.session_state.csv_handler._load_csv()
                    
                    with csv_display.container():
                        st.subheader("Current CSV Data")
                        st.dataframe(st.session_state.csv_handler.df)
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
