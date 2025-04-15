from typing import List, Optional

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter

import os
import tempfile
from langchain.document_loaders import PyPDFLoader
from langchain_community.callbacks import get_openai_callback
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from schemas_diff import Other_Benefits


from src.utils.retrieval_prompts import RETRIEVAL_SYSTEM_PROMPT_2,RETRIEVAL_HUMAN_PROMPT_TEMPLATE_3,RETRIEVAL_HUMAN_PROMPT_TEMPLATE_4

from  dotenv import load_dotenv

load_dotenv(override=True)
embeddings = OpenAIEmbeddings()

# Initialize text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=[
    "\n\n", 
    "\n", 
    r'(?<=[.!?]) +',
    " ", 
    ""
]
)
class Death_Benefit_Payment_Option_Field(BaseModel):
    value: Optional[str] = Field(
        ..., description="Payout options of the amount to be paid to the nominee in the event of the policyholder's death"
    )
    page_number: Optional[str] = Field(
        ..., description="Page number where the field was extracted from"
    )
    chunks: Optional[List[str]] = Field(
        ...,
        description="Source of the chunks, keep it empty if null",
    )


class Plan_Options_Field(BaseModel):
    value: Optional[str] = Field(
        ..., description="Available plan options with their plan description and statistical details"
    )
    page_number: Optional[str] = Field(
        ..., description="Page number where the field was extracted from"
    )
    chunks: Optional[List[str]] = Field(
        ...,
        description="Source of the chunks, keep it empty if null",
    )

# Define a custom prompt to provide instructions and any additional context.
# 1) You can add examples into the prompt template to improve extraction quality
# 2) Introduce additional parameters to take context into account (e.g., include metadata
#    about the document from which the text was extracted.)
prompt_plan_options = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            RETRIEVAL_SYSTEM_PROMPT_2
        ),
        (
            "human", 
            "Extract and summarize the plan options from the given text, with each descriptive line for each of the plan options  {text}"
        ),
    ]
)

prompt_other_benefits = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            RETRIEVAL_SYSTEM_PROMPT_2           
        ),
        (
            "human", 
            RETRIEVAL_HUMAN_PROMPT_TEMPLATE_4
        ),
    ]
)

prompt_surrender_options = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            RETRIEVAL_SYSTEM_PROMPT_2
        ),
        (
            "human", 
            "What are the surrender value factor for surrender benefits of the policy/product, extract from the given text. {text}"
        ),
    ]
)

# prompt_premium_payment_option = ChatPromptTemplate.from_messages(
llm = init_chat_model(os.environ.get("MODEL_OPENAI"), model_provider="openai", temperature=0,verbose=True)

def init_vectorstore(uin):
    """
    Initialize and return a Chroma vector store instance for the given UIN.

    Args:
        uin (str): Unique Identifier Number for the policy/product.

    Returns:
        Chroma: An instance of the Chroma vector store.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    persistent_directory = os.path.join(current_dir, "db", f"chroma_db_{uin}")
    
    if not os.path.exists(persistent_directory):
        print(f"----Vector DB does not exist for UIN {uin}, creating a new one----")
        os.makedirs(persistent_directory)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    db = Chroma(persist_directory=persistent_directory, embedding_function=embeddings)

    return db


def print_formatted_prompt(inputs):
    """Print the fully formatted prompt before it goes to the LLM"""
    query = inputs["query"]
    docs = inputs["text"]
    
    # Format the documents into a string
    docs_text = "\n\n".join([doc.page_content for doc in docs])
    
    # Get the exact prompt that will be sent to the LLM
    formatted_prompt = prompt_other_benefits.format_prompt(
        text=docs_text,
        query=query
    )
    
    print("\n==========FULLY FORMATTED PROMPT==========")
    print(formatted_prompt.to_string())  # Convert the prompt messages to string
    print("==========================================\n")
    
    return inputs

def create_chunks(uploaded_file):
    """
        Create text chunks from the uploaded PDF file.
    """


    db = init_vectorstore("107N129V03") # manually adding the UIN for now 
    retriever = db.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": 3, "score_threshold": 0.2}
    ) 
  
    # Test the retriever directly
    query = "What are the optional/other benefits(if available) for example child care, adoption, marriage, life stage benefits etc. in the policy?"
    retrieved_docs = retriever.invoke(query)
    
    # Debug the retrieved documents
    print("\n----- RETRIEVED DOCUMENTS FOR QUERY -----")
    print(f"Query: {query}")
    print(f"Total documents retrieved: {len(retrieved_docs)}")
    for i, doc in enumerate(retrieved_docs):
        print(f"\nDOCUMENT {i+1}:")
        print(f"Content: {doc.page_content}")
        print(f"Metadata: {doc.metadata}")

    extractor = prompt_other_benefits| llm.with_structured_output(
        schema=Other_Benefits,
        include_raw=False,
    )
    
    policy_name = "Kotak e-Term"
    # Define the RAG chain using LCEL
    rag_extractor = {
        "text": lambda params: retriever.invoke(params["query"]),
        "query": RunnablePassthrough()
    } | RunnableLambda(print_formatted_prompt) |  extractor

    results = rag_extractor.invoke({"query": query})

    
    print("---------Obtained Basic Policy Details ------------")
    print(results)
    print("---------Finished Extraction ------------")
def main():
    # Example usage
    with open("/home/cloudcraftz/WORK/LANGCHAIN_LEARNING/Kotak-e-Term-Plan.pdf", "rb") as f:
        create_chunks(f)

if __name__ == "__main__":
    main()
