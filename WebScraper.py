from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# web domain 
domain = "https://www.agnoshealth.com/"

#Base URL of the webboard forum
base_url = "https://www.agnoshealth.com/en/forums/search"

#number of forum pages to scrape
max_page = 10

#Directory of Vector database 
db_location = "./chroma_langchain_db"

#model that use to embed text 
embeddings = OllamaEmbeddings(model="bge-m3")

#Chroma vector databse
vector_store = Chroma(
    collection_name="Agnos_forum",
    persist_directory=db_location,
    embedding_function=embeddings
)

#function to get forum urls in a page
def get_forum_url(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")

    forum_urls = []
    for a in soup.find_all("a", class_="undefined", href=True):
        relative = a["href"]
        full_url = urljoin(domain, relative)
        forum_urls.append(full_url)

    return forum_urls  

#load data from website
def load_page(url):
    loader = WebBaseLoader(
    web_paths=(url,),
    )
    docs = loader.load()

    return docs

#function to split data to chunk
def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )
    chunked_docs = text_splitter.split_documents(documents)

    return chunked_docs

#function to store data in database
def index_docs(documents):
    vector_store.add_documents(documents)

#function to store every forum in a page to database
def index_SubForum (base_url):
    urls = get_forum_url(base_url)
    for url in urls :
        docs = load_page(url)
        chunked_docs = split_text(docs)
        index_docs(chunked_docs)

#function to store every forum in 10 pages(max_page) to database
def index_page(page_url, max_page ):
    for page in range(1,max_page +1):
        url = page_url + f"?page={page}"
        print(f"url:{url}")
        print(f"page:{page}")
        index_SubForum (url)


#Start scraping data from the webboard and store it in the Chroma vector DB
index_page(base_url, max_page )







