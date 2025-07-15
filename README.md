

## How to Run This RAG Chatbot App

You have two options to run this application:



###  🐍Option 1: Run Locally 

1. **Clone this repository**:

   ```bash
   git clone https://github.com/PunnnYutt/Task1-LLM-chatbot.git
   ```

2. **Install Ollama** https://ollama.com/download

3. **Download required models**:

   ```bash
   ollama pull llama3.2
   ollama pull bge-m3
   ```

4. **Create and activate a virtual environment**:

   ```bash
   python -m venv venv
   venv\Scripts\activate 
   ```

5. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

6. **Run the app**:

   ```bash
   streamlit run ChatBot.py
   ```

7. **Open your browser** and go to: http://localhost:8501

---

### 🐳 Option 2: Run with Docker

1. **Clone this repository**:

   ```bash
   git clone git clone https://github.com/PunnnYutt/Task1-LLM-chatbot.git
   ```

2. **Build the Docker image**:

   ```bash
   docker build -t chatbot .
   ```

3. **Run the container**:

   ```bash
   docker run -d -p 8501:8501 --name chatbot-container chatbot
   ```
   Wait for the container to finish installing the models and starting the app.

4. **Access the app** in your browser: http://localhost:8501

5. **To stop the container**:

   ```bash
   docker stop chatbot-container
   ```
---
## 📓 Note on web scraping

I limited the scraping to the first 10 pages of the forum due to time constraints and to reduce the load on my local machine.


