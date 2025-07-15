FROM ollama/ollama:latest

EXPOSE 8501

WORKDIR /RagChat
COPY ChatBot.py /RagChat
COPY chroma_langchain_db/ /RagChat/chroma_langchain_db/
COPY requirements.txt /RagChat

RUN apt update && apt install -y python3 python3-pip
RUN pip install --break-system-packages -r requirements.txt


# Override ENTRYPOINT to allow shell use
ENTRYPOINT []

# Run Ollama in background, then your app
CMD /bin/sh -c "ollama serve &sleep 5 && ollama pull llama3.2 && ollama pull bge-m3 && streamlit run ChatBot.py"

