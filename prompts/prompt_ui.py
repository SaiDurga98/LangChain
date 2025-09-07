from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import streamlit as st
from langchain_core.prompts import PromptTemplate,load_prompt


load_dotenv() # loads environment variables from a .env file
model = ChatOpenAI() # LangChain’s chat-model wrapper for OpenAI.

st.header('Reasearch Tool') # Streamlit - UI framework to build the little web page.

paper_input = st.selectbox( "Select Research Paper Name", ["Attention Is All You Need", "BERT: Pre-training of Deep Bidirectional Transformers", "GPT-3: Language Models are Few-Shot Learners", "Diffusion Models Beat GANs on Image Synthesis"] )

style_input = st.selectbox( "Select Explanation Style", ["Beginner-Friendly", "Technical", "Code-Oriented", "Mathematical"] ) 

length_input = st.selectbox( "Select Explanation Length", ["Short (1-2 paragraphs)", "Medium (3-5 paragraphs)", "Long (detailed explanation)"] )

# loads a saved/serialized LangChain prompt (e.g., from template.json). PromptTemplate is the class that type represents.
template = load_prompt('template.json')

# template | model uses LangChain’s Runnable composition operator (|) to build a pipeline:
# The prompt template receives your inputs and formats a proper prompt/messages.
# The chat model is invoked with that prompt.
# chain.invoke({...}) passes the three values that the prompt expects.
# result is a ChatMessage (from the model). .content is the text the model generated.
# st.write(...) renders it in the Streamlit app.
if st.button('Summarize'):
    chain = template | model
    result = chain.invoke({
        'paper_input':paper_input,
        'style_input':style_input,
        'length_input':length_input
    })

    st.write(result.content)