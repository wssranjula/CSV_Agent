from dotenv import load_dotenv 
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents import create_csv_agent
from langchain.document_loaders.csv_loader import CSVLoader
import pandas as pd

load_dotenv()

def main():
    st.set_page_config(page_title="Ask CSV")
    st.header("Ask your Question 💬")
    uploaded_file = st.file_uploader("Upload a CSV File", type=["csv"])
    api = st.secrets.get("OPENAI_API_KEY")

    if uploaded_file:
        st.write("File uploaded successfully")
        df = pd.read_csv(uploaded_file)
        
        llm = ChatOpenAI(temperature=0, openai_api_key=api, model="gpt-3.5-turbo-0613")
        data = df.to_dict()
        agent = create_csv_agent(
            llm,
            data,
            verbose=True,
            agent_type=AgentType.OPENAI_FUNCTIONS,
        )

        prompt = st.text_input("Your question:")
        if prompt:
            st.write("🧠 Thinking...")
            st_callback = StreamlitCallbackHandler(st.container())
            response = agent.run(prompt, callbacks=[st_callback])
            st.write(response)
            
if __name__ == '__main__':
    main()
