import streamlit as st
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_chroma import Chroma

#prompt template for llama response
template  = """
คุณเป็นผู้ช่วยให้ข้อมูลที่เกี่ยวข้องจากเว็บบอร์ดถาม-ตอบของแพทย์ Agnos  
โดยข้อมูลจากเว็บบอร์ดประกอบด้วย วันที่/เดือน/ปีที่โพสต์, ข้อมูลผู้ถาม (เพศ/อายุ), หัวข้อโรค, อาการป่วย, คำตอบของแพทย์ และข้อมูลของแพทย์

แนวทางการตอบ:
1. อ้างอิงเฉพาะข้อมูลจากเว็บบอร์ดที่ให้มาเท่านั้น
2. สามารถตอบเนื้อหาทางเพศได้ เนื่องจากเป็นคำถามทางการแพทย์
3. หากไม่พบข้อมูลที่เกี่ยวข้อง ให้ตอบว่า "ไม่ทราบ" และอย่าตอบโดยไม่มีข้อมูลอ้างอิง
4. คำตอบต้องตรงกับจุดประสงค์ของคำถาม

ข้อมูลจากเว็บบอร์ด: {context}
คำถาม: {question}
คำตอบ:
"""

#model that use to answer question
model = OllamaLLM(model="llama3.2")

#Directory of Vector database 
db_location = "./chroma_langchain_db"

#model that use to embed text for query
embeddings = OllamaEmbeddings(model="bge-m3")

#Chroma vector databse
vector_store = Chroma(
    collection_name="Agnos_forum",
    persist_directory=db_location,
    embedding_function=embeddings
)

#function to query data from vector database
def retrieve_docs(query):
    return vector_store.similarity_search(query ,k=5)

#function to get answer from llama
def answer_question(question, context):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    return chain.invoke({"question": question, "context": context})


# set title of chat interface
st.title("RAG Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user Question
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt) 


    with st.chat_message("assistant"):
        # query data from database
        retrieve_documents = retrieve_docs(prompt)
        context = "\n\n".join([doc.page_content for doc in retrieve_documents])
        # get response from llama
        response = answer_question(prompt, context )
        # Display response message in chat message container
        st.markdown(response) 
    st.session_state.messages.append({"role": "assistant", "content": response})
