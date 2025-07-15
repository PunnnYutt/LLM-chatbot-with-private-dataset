FROM ollama/ollama:latest

EXPOSE 8501

WORKDIR /RagChat
COPY ChatBot.py /RagChat
COPY chroma_langchain_db /RagChat
COPY requirements.txt /RagChat

RUN apt update && apt install -y python3 python3-pip
RUN pip install -r requirements.txt
RUN ollama pull llama3.2
RUN ollama pull bge-m3

CMD ollama serve & \
    sleep 2 && \
    ollama pull llama3.2 && \
    ollama pull bge-m3 && \
    streamlit run app.py
