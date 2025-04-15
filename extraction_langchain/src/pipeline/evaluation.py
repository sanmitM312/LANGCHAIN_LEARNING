import os
import streamlit as st
import json
from typing import List
from dotenv import load_dotenv
# from sentence_transformers import SentenceTransformer
import numpy as np


from utils.schemas import TUnitLinkedPlan,TUnitLinkedPlanField
from utils.evaluation_prompts import USER_PROMPT_TEMPLATE,SYSTEM_PROMPT

from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage


load_dotenv(override=True)
# sentence_model = SentenceTransformer('all-MiniLM-L6-v2') 

def compare_json_files(uin: str, output_data: TUnitLinkedPlan) -> dict:
    """
    Compare extracted policy details with ground truth JSON file if available.
    """
    actual_file_path = f"../ground_truth/tulip/{uin}.json"
    
    # Check if the ground truth JSON file exists
    if not os.path.exists(actual_file_path):
        return None  # Return None if file does not exist
        
    
    actual_data = load_json(actual_file_path)
    if actual_data is None:
        return {"error": "Failed to load actual data."}

    results = {}
    total_score = 0
    key_count = 0

    for key, actual_value in actual_data.items():
        output_value = getattr(output_data, key, None)
        if output_value:
            score = compare_key_values_llm(key,actual_value, output_value.value)
            if score != -1:  # Only count valid scores
                total_score += score
                key_count += 1
            results[key] = score

    average_score = total_score / key_count if key_count else 0

    eval_response = {"results": results, "average_score_normalized": average_score}

    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, '..','../evaluation'))
    eval_dir = os.path.join(parent_dir, "eval_data")
    output_file = os.path.join(eval_dir, f"{uin}_eval.json")
    output_dir = os.path.dirname(output_file)  # Extract directory path
    os.makedirs(output_dir, exist_ok=True)  # Create directory if not exists
    
    with open(output_file, "w") as f:
        json.dump(eval_response, f, indent=4)

    return eval_response

# def compare_key_values_(key: str, actual_value: str, output_value: str) -> int:
#     emb1 = sentence_model.encode(actual_value)
#     emb2 = sentence_model.encode(output_value)
#     return np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))

def compare_key_values_llm(key,actual_value, output_value) -> int:
    """
    Compare individual key-value pairs using OpenAI and return a similarity score.
    """
    actual_value_str = str(actual_value)
    output_value_str = str(output_value)

    user_prompt = USER_PROMPT_TEMPLATE.format(
        actual_value=actual_value_str, 
        output_value=output_value_str
    )
    try:

        chat = ChatOpenAI(
            model=os.environ.get("MODEL_OPENAI"), 
            temperature=0.2,   
        )      
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=user_prompt)
        ]

        comparison_score = chat.invoke(messages)
        # print(f"Comparison Score {key} {actual_value_str} {output_value_str}: {comparison_score.content.strip()}")
        score = comparison_score.content.strip()
        if score == 'N/A':
            return -1

        return int(score) - 1 // 4  # Normalize to 0-1 scale
    except ValueError as ve:
        st.error(f"ValueError during comparison API call: {ve}")
        return -1
    except Exception as e:
        st.error(f"Error during comparison API call: {e}")
        return -1  # Return -1 for errors

def load_json(file_path: str):
    """
    Load a JSON file from the given path.
    """
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except Exception as e:
        st.error(f"Failed to load JSON file: {e}")
        return None



def merge_policy_and_accuracy_tables(
    policy_details: TUnitLinkedPlan, accuracy_data: dict
) -> List[dict]:
    """
    Merge policy details and accuracy JSON into a single table for display.
    If accuracy_data is None, "N/A" will be shown for the Accuracy Score.
    """
    merged_table = []
    policy_data = policy_details.model_dump()

    for key, field in policy_data.items():
        if field:  # Only include fields that are not None
            merged_table.append({
                "Field": key.replace("_", " ").title(),
                "Value": field.get("value", "N/A"),
                "Page Number": field.get("page_number", "N/A"),
                "Accuracy Score": accuracy_data.get(key, "N/A") if accuracy_data else "N/A"
            })

    return merged_table

