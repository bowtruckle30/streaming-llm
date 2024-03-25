import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage  
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI


load_dotenv(override=True)

# app config
st.set_page_config(page_title='Streaming Bot', page_icon='🤖')
st.title('Streaming Bot')

# initialize session chat_history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [AIMessage('Hi, I am a bot. How can I help you?')]

# get response from langugage model
def get_response(query, chat_history):
    template = '''You are a helpful assistant. Answer the following questions considering the history of the conversation.
    Chat history: {chat_history}
    User question: {user_question}'''
    
    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI()
    chain = prompt | llm | StrOutputParser()

    return chain.stream({
        "chat_history": chat_history,
        "user_question": query
    })

# conversation
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message('Human'):
            st.markdown(message.content)
    if isinstance(message, AIMessage):
        with st.chat_message('AI'):
            st.markdown(message.content)

# user input
user_query = st.chat_input('Your message')
if user_query is not None and user_query != '':
    st.session_state.chat_history.append(HumanMessage(user_query))

    with st.chat_message('Human'):
        st.markdown(user_query)
    
    with st.chat_message('AI'):
        ai_response = st.write_stream(get_response(user_query, st.session_state.chat_history))

    st.session_state.chat_history.append(AIMessage(ai_response))