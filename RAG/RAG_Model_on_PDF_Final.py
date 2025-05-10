from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import VectorDBQA,RetrievalQA,LLMChain
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
import tempfile
from dotenv import load_dotenv
import os


# Custom CSS for a cleaner UI
st.markdown("""
    <style>
    .chat-bubble-user {
        background-color: #DCF8C6;
        color: black;
        padding: 10px 15px;
        border-radius: 18px;
        margin: 8px;
        text-align: right;
        width: fit-content;
        margin-left: auto;
        font-size: 16px;
    }
    .chat-bubble-model {
        background-color: #F1F0F0;
        color: black;
        padding: 10px 15px;
        border-radius: 18px;
        margin: 8px;
        text-align: left;
        width: fit-content;
        margin-right: auto;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# Load environment variables from .env file
load_dotenv()

# Retrieve the key
api_key=os.getenv('GOOGLE_API_KEY')

# Title
st.markdown('<h1 class="main-title">PDF-Based Chatbot</h1>', unsafe_allow_html=True)
st.markdown('<h3 class="sub-title">Chat with Any PDF Using AI !</h3>', unsafe_allow_html=True)
file= st.file_uploader('Upload the file',type=['pdf'])

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(file.read())
        temp_file_path = temp_file.name

    loader = PyPDFLoader(temp_file_path)

    # if file is not None:
    #     # Document Loader
    #     loader=PyPDFLoader(file)
    documents=loader.load()
    # Text Splitting
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=150)
    text=text_splitter.split_documents(documents)

    #Setting Up the embedding model
    embeddings=GoogleGenerativeAIEmbeddings(
        model='models/embedding-001',
       google_api_key=api_key,
       task_type='retrieval_query'
    )
    #Step-5 :Getting the embeddings and storing them in VectorDB(Chroma or FIASS)
    #create the vector store and store the embeddings init
    vectordb=Chroma.from_documents(documents=text,embedding=embeddings)

    # Step-6:Make the Prompt Template
    # here we are controlling the model with the propmt template

    prompt_template="""
    ## Safety and Respect Come First!

    You are programmed to be a helpful and harmless AI. You will not answer requests that promote:

    * **Harassment or Bullying:** Targeting individuals or groups with hateful or hurtful language.
    * **Hate Speech:**  Content that attacks or demeans others based on race, ethnicity, religion, gender, sexual orientation, disability, or other protected characteristics.
    * **Violence or Harm:**  Promoting or glorifying violence, illegal activities, or dangerous behavior.
    * **Misinformation and Falsehoods:**  Spreading demonstrably false or misleading information.

    **How to Use You:**

    1. **Provide Context:** Give me background information on a topic.
    2. **Ask Your Question:** Clearly state your question related to the provided context.

    **Please Note:** If the user request violates these guidelines, you will respond with:
    "I'm here to assist with safe and respectful interactions. Your query goes against my guidelines. Let's try something different that promotes a positive and inclusive environment."

    ##  Answering User Question:

    Answer the question as precisely as possible using the provided context. The context can be from different topics. Please make sure the context is highly related to the question. If the answer is not in the context, you only say "answer is not in the context".

    Context: \n {context}
    Question: \n {question}
    Answer:
    """

    prompt = PromptTemplate(template = prompt_template, input_variables=['context','question'])


    # Setting up the Chatmodel for retrieval
    # setting up the Chatmodel
    from google.generativeai.types.safety_types import HarmBlockThreshold,HarmCategory

    safety_settings={HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT:HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH:HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT:HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT:HarmBlockThreshold.BLOCK_LOW_AND_ABOVE

    }
    chat_model=ChatGoogleGenerativeAI(
        model='gemini-2.0-flash',
        google_api_key=api_key,
        temperature=0.3, #Creativity Temperature
        safety_settings=safety_settings
    )


    # selecting one retriver to retrive the most relevant chunks based on the user's question.
    retriever_from_llm=MultiQueryRetriever.from_llm(retriever=vectordb.as_retriever(search_kwargs={'k':2}),llm=chat_model)

    qa_chain=RetrievalQA.from_chain_type(llm=chat_model,
                                     retriever=retriever_from_llm,
                                     return_source_documents=True,
                                     chain_type='stuff',
                                     chain_type_kwargs={'prompt':prompt})

    query=st.text_input('Enter the Question:')
    if st.button('Get Answer'):
      result = qa_chain({'query': query})
      st.session_state.chat_history.append(("You", query))
      st.session_state.chat_history.append(("Bot", result['result']))

      for speaker, message in st.session_state.chat_history:
          if speaker == "You":
            st.markdown(f"<div class='chat-bubble-user'>👨: {message}</div>", unsafe_allow_html=True)
          else:
            st.markdown(f"<div class='chat-bubble-model'>🤖: {message}</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
    <hr style="border: 0; height: 1px; background-color: #000000;">
    <div style="text-align: center; font-size: 14px; color: #000000;">
        Built with LangChain, Google Gemini, and Streamlit for interactive document Q&A.
    </div>
    """, unsafe_allow_html=True)

