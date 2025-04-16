
import streamlit as st
import sys
from typing import List

from utils.schemas import TUnitLinkedPlan, TUnitLinkedPlanField
from utils.evaluation_prompts import USER_PROMPT_TEMPLATE,SYSTEM_PROMPT
from pipeline.preprocess import preprocess,extract_basic_policy_details,store_in_vectordb,create_chunks
from pipeline.retrieval import init_retrieval
from pipeline.evaluation import merge_policy_and_accuracy_tables, compare_json_files
import json
import os

from json_to_excel import add_row_to_excel

def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extract text from an uploaded PDF file and format it by page.
    """
    try:
       return "<PDF TEXT/>"
    except Exception as e:
        st.error(f"An error occurred while extracting text: {e}")
        return None


def write_to_excel(updated_policy_details: TUnitLinkedPlan) -> None:
    """Write the updated policy details to an Excel file."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
    excel_data_dir = os.path.join(parent_dir,"results")
    excel_path = os.path.join(excel_data_dir, "results_third.xlsx")
    output_data_dir = os.path.join(parent_dir,"neo_extracted_data")
    json_file = os.path.join(output_data_dir, f"{updated_policy_details.product_uin.value}_rag.json")
    add_row_to_excel(json_file, excel_path)
def update_rag_fields(
    policy: TUnitLinkedPlan,
    rag_fields: dict[str,TUnitLinkedPlanField]
) -> TUnitLinkedPlan:
    """Safely update the rag fields and write to json file"""


    # Update the policy with RAG fields
    for key, value in rag_fields.items():
        if policy.__getattribute__(key).value != "Not Available" and rag_fields[key] == "Not available":
            rag_fields[key] = policy.__getattribute__(key).value

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
        uin = sys.argv[1]
        policy_name = sys.argv[2]

        rag_fields = init_retrieval(uin,policy_name)

        with open(f'../neo_extracted_data/{uin}_rag.json', 'r') as file:
            data = json.load(file)

        basic_policy_details = TUnitLinkedPlan(**data)

        if rag_fields:
            updated_policy_details = update_rag_fields(basic_policy_details,rag_fields)

            uin = updated_policy_details.product_uin.value  # Example UIN

            comparison_result = compare_json_files(uin, updated_policy_details)

            print("----Writing to Excel file----")
            write_to_excel(updated_policy_details)
            print("----Excel file updated----")
            
            # print(f"comparison result {uin}: {comparison_result}")

            if comparison_result is None:
                st.warning("Ground truth data not available. Accuracy scores will be shown as N/A.")
                table = merge_policy_and_accuracy_tables(updated_policy_details, {})
                st.subheader("Policy Details")
                st.table(table)
            elif "error" in comparison_result:
                st.error(comparison_result["error"])
            else:
                results_without_average_score = {
                    key: value for key, value in comparison_result['results'].items()
                }
                with_rag_table = merge_policy_and_accuracy_tables(updated_policy_details, results_without_average_score)
                st.subheader("Policy Details")
                st.table(with_rag_table)
                st.write(f"**Average Score**: {comparison_result['average_score_normalized']:.2f}")
                
                
        else:
            st.error("Failed to extract using RAG")
        
        

if __name__ == '__main__':
    main()