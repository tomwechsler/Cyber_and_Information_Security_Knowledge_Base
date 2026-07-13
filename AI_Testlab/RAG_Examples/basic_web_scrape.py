# This script demonstrates how to scrape a web page, split the content into chunks, create embeddings for the chunks,
# persist the vector store, and use a RAG chain to answer questions based on the scraped content.


# Import the required libraries
import os

from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_text_splitters import CharacterTextSplitter

# Define the persistent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
db_dir = os.path.join(current_dir, "db")
persistent_directory = os.path.join(db_dir, "hacker_training")

# --- 1. Scrape and Load Web Content ---
urls = ["http://zero.webappsecurity.com"]
loader = WebBaseLoader(urls)
documents = loader.load()

# --- 2. Split the Scraped Content into Chunks ---
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

print("\n--- Document Chunks Information ---")
print(f"Number of document chunks: {len(docs)}")
print(f"Sample chunk:\n{docs[0].page_content}\n")

# --- 3. Create Embeddings ---
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# --- 4. Create and Persist the Vector Store ---
if not os.path.exists(persistent_directory):
    print(f"\n--- Creating vector store in {persistent_directory} ---")
    db = Chroma.from_documents(docs, embeddings, persist_directory=persistent_directory)
    print(f"--- Finished creating vector store in {persistent_directory} ---")
else:
    print(f"Vector store {persistent_directory} already exists. No need to initialize.")
    db = Chroma(persist_directory=persistent_directory, embedding_function=embeddings)

# --- 5. Create the Retriever ---
retriever = db.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 3, "score_threshold": 0.5},
)

# --- 6. Define the RAG Chain ---
prompt_template = """
You are a cybersecurity expert. Answer the question based only on the following context:

{context}

Question: {question}
"""

prompt = ChatPromptTemplate.from_template(prompt_template)

llm = ChatOllama(model="qwen2.5:14b")


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# --- 7. Invoke the Chain and Get the Answer ---
if __name__ == "__main__":
    query = "What is zero.webappsecurity.com all about?"

    relevant_docs = retriever.invoke(query)

    print("\n--- Relevant Documents from the vector store ---")
    for i, doc in enumerate(relevant_docs, 1):
        print(f"Document {i}:\n{doc.page_content}\n")
        if doc.metadata:
            print(f"Source: {doc.metadata.get('source', 'Unknown')}\n")

    print("\n--- AI-Generated Answer ---")
    response = rag_chain.invoke(query)
    print(response)
