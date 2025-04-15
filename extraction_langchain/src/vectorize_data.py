
import streamlit as st

from typing import List

from utils.schemas import TUnitLinkedPlan, TUnitLinkedPlanField
from utils.evaluation_prompts import USER_PROMPT_TEMPLATE,SYSTEM_PROMPT
from pipeline.preprocess import preprocess,extract_basic_policy_details,store_in_vectordb,create_chunks
from pipeline.retrieval import init_retrieval
from pipeline.evaluation import merge_policy_and_accuracy_tables, compare_json_files
import json
import os

def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extract text from an uploaded PDF file and format it by page.
    """
    try:
       return "<PDF TEXT/>"
    except Exception as e:
        st.error(f"An error occurred while extracting text: {e}")
        return None



def update_rag_fields(policy: TUnitLinkedPlan,rag_fields: dict[str,TUnitLinkedPlanField]) -> TUnitLinkedPlan:
    """Safely update the rag fields and write to json file"""


    # Update the policy with RAG fields
    new_policy = policy.model_copy(update=rag_fields)

    # Define the output directory and file path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, '..'))

    data_dir = os.path.join(parent_dir,"neo_extracted_data")
    output_file = os.path.join(data_dir, f"{new_policy.product_uin.value}_rag.json")

    # Write the updated policy to a JSON file
    try:
        with open(output_file, "w") as f:
            json.dump(new_policy.model_dump(), f, indent=4)
    except Exception as e:
        st.error(f"An error occurred while writing to file: {e}")

    return new_policy

def main():

    st.title("Policy Details Extractor")
    st.write("Upload PDF containing policy details, and this app will extract and display \
        the structured information for you")

    uploaded_file = st.file_uploader("Upload a pdf file", type="pdf")

    if uploaded_file:
        st.write("Processing your file...")

        pdf_text = extract_text_from_pdf(uploaded_file)
        if pdf_text:
            chunks,pdf_text = create_chunks(uploaded_file)
            print("\n--- Document Chunks Information ---")
            print(f"Number of page chunks: {len(chunks)}")

            # TUnitLinkedPlan instance 
            basic_policy_details = extract_basic_policy_details(pdf_text)
            
            print("---------Obtained Basic Policy Details ------------")

            print(basic_policy_details.product_uin.value)
            print(basic_policy_details.product_name.value)
            # initialize the vector store
            store_in_vectordb(chunks,basic_policy_details.product_uin.value,db_dir="neo_db")

            # if json file does not exist, write the json file.
            # Define the output directory and file path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.abspath(os.path.join(current_dir, '..'))

            data_dir = os.path.join(parent_dir,"neo_extracted_data")
            output_file = os.path.join(data_dir, f"{basic_policy_details.product_uin.value}_rag.json")

            # Write the updated policy to a JSON file
            if not os.path.exists(output_file):
                print("Output file of RAG does not exist. Initializing RAG output...")
                try:
                    with open(output_file, "w") as f:
                        json.dump(basic_policy_details.model_dump(), f, indent=4)
                except Exception as e:
                    st.error(f"An error occurred while writing to file: {e}")
                print("\n --- Finished writing to rag file ---")
            else : 
                print("-------- Rag file already exists. No need to initialize. ---------")
            
                
if __name__ == '__main__':
    main()