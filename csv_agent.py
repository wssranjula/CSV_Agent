from dotenv import load_dotenv 
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents import create_csv_agent





st.set_page_config(page_title="Ask CSV")
st.header("Ask your Question 💬")

uploaded_file = st.file_uploader("Upload a CSV File",type=["csv"])

if uploaded_file:
    st.write("File uploaded successfully")
    

def main():
    load_dotenv()
    
    if uploaded_file is not None:
       llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
       
       path = uploaded_file.name
      

       agent = create_csv_agent(
        ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
            path,
            verbose=True,
            agent_type=AgentType.OPENAI_FUNCTIONS,
)                        
        
       if prompt := st.chat_input():
            st.chat_message('user').write(prompt)
            with st.chat_message("assistant"):
                st.write("🧠 Thinking...")
                st_callback =StreamlitCallbackHandler(st.container())
                response = agent.run(prompt,callbacks=[st_callback])
                st.write(response)
            
        
if __name__ == '__main__':
    main()