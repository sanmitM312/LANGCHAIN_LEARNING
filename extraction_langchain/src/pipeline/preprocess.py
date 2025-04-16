
import PyPDF2
import streamlit as st
import tempfile
import os
from textwrap import dedent
from dotenv import load_dotenv

from openai import OpenAI

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings 
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage,HumanMessage
from langchain_community.vectorstores import Chroma
from langchain_community.callbacks import get_openai_callback

from utils.retrieval_prompts import T_PURE_TERM_PLAN
from utils.schemas import TUnitLinkedPlan

from langchain.document_loaders import PyPDFLoader
import tiktoken

load_dotenv(override=True)

# Initialize embeddings
embeddings = OpenAIEmbeddings()
encoding = tiktoken.get_encoding("cl100k_base")


# Initialize text splitter
# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=700,
#     chunk_overlap=60,
#     separators=["\n\n","\n","(?<=\. )"," ", ""]
# )
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
    separators=["\n\n", "(?<=\. )","\n"," ", ""]
)
# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=750,
#     chunk_overlap=50,
#     separators=[
#         "\n\n",          # Split on paragraphs
#         "\n---+\n",      # Split on horizontal lines (common in tables)
#         r'\n\s*\|\s*\n', # Split on pipe-separated table rows
#         r'\n\s{2,}',     # Split on lines with 2+ spaces (common in tabular data)
#         "\n",            # Split on newlines
#         r'(?<=\. )',     # Split after sentences
#         r'\s{4,}',       # Split on 4+ whitespace characters (tabular columns)
#         " ",             # Split on single spaces
#         ""
#     ]
# )

# return texts in chunks and the entire text
def create_chunks(uploaded_file):
    """
        Create text chunks from the uploaded PDF file.
    """

    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name
    

    # Load PDF with page numbers(metadata feature)
    loader = PyPDFLoader(tmp_path)
    pages = loader.load()
    os.unlink(tmp_path)
    
    pdf_text = " ".join([page.page_content for page in pages])
    
    tokens = encoding.encode(pdf_text)
    num_tokens = len(tokens)
    print(f"Number of tokens in the document: {num_tokens}")

    if(num_tokens > 100000):
        num_pages = len(pages)
        first_ten_pages = pages[:10]
        last_five_pages = pages[-5:]
        pdf_text = " ".join([page.page_content for page in first_ten_pages + last_five_pages])
        print(f"Number of tokens in the first and last 10 pages: {len(encoding.encode(pdf_text))}")
    
    chunks = text_splitter.split_documents(pages)

    return chunks,pdf_text


def store_in_vectordb(chunks,uin,db_dir="db"):
    """
    Store the chunks in a vector database using Chroma.
    """

    print("\n--- Creating Embeddings ----")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, '..','..'))
    db_dir = os.path.join(parent_dir, db_dir)
    persistent_directory = os.path.join(db_dir, f"chroma_db_{uin}")

    if not os.path.exists(persistent_directory):
        print("Persistent directory does not exist. Initializing vector store...")
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small"
        )
        
        print("\n--- Creating and persisting vector store ----")
        db = Chroma.from_documents(
            chunks,embeddings,persist_directory=persistent_directory
        )

        print("\n --- Finished creating and persisting vector store")
    else : 
        print("Vector store already exists. No need to initialize.")

def extract_basic_policy_details(text:str)->TUnitLinkedPlan:
    """
        extract basic policy details using prompt engineering
    """
    print("---------Starting Basic Extraction ------------")
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        chat = ChatOpenAI(
            model=os.environ.get("MODEL_OPENAI"), 
            temperature=0, 
        )
        
        messages = [
            SystemMessage(content=dedent(T_PURE_TERM_PLAN)),
            HumanMessage(content=text)
        ]
        
        # with get_openai_callback() as callback:
        structured_llm = chat.with_structured_output(TUnitLinkedPlan)
        response = structured_llm.invoke(messages)
            # write the cost to a file
            # current_dir = os.path.dirname(os.path.abspath(__file__))
            # parent_dir = os.path.abspath(os.path.join(current_dir, '..','..'))
            
            # data_dir = os.path.join(parent_dir,"cost")
            # output_file = os.path.join(data_dir, f"{response.product_uin.value}_cost.txt")
            # with open(output_file, "w") as f:
            #     f.write(f"Tokens used: {callback.total_tokens}\n")
            #     f.write(f"Cost: ${callback.total_cost:.4f}\n")

        

        print("---------Ending Basic Extraction ------------")
        return response #type: ignore
    
    except Exception as e:
        st.error(f"Error during API call: {e}")
        return TUnitLinkedPlan()


def preprocess(uploaded_file):
    # chunk the documents 
    chunks,pdf_text = create_chunks(uploaded_file)

    print("\n--- Document Chunks Information ---")
    print(f"Number of page chunks: {len(chunks)}")

    print("The chunks are : ")
    for i, chunk in enumerate(chunks[:5], start=1):
        print(f"Chunk {i}: {chunk.page_content}\n")


    # TUnitLinkedPlan instance 
    basic_response = extract_basic_policy_details(pdf_text)

    # store in vectordb
    store_in_vectordb(chunks,basic_response.product_uin.value)

    return basic_response





