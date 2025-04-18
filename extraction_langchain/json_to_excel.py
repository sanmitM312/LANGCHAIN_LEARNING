import json
import os
import pandas as pd
import sys 



def add_rows_to_excel(json_dir, excel_path):
    # Check if the directory exists
    if not os.path.exists(json_dir):
        raise FileNotFoundError(f"The directory {json_dir} does not exist.")
    
    # Initialize an empty list to store rows
    rows = []

    # Process each JSON file in directory
    for filename in os.listdir(json_dir):
        if filename.endswith('.json'):
            with open(os.path.join(json_dir, filename)) as f:
                data = json.load(f)
                
                # Extract values from each field
                row = {key: value['value'] for key, value in data.items()}
                rows.append(row)

    # Create DataFrame and save to Excel
    df = pd.DataFrame(rows)
    df = df.T  # Transpose the DataFrame
    df.columns = df.iloc[0]  # Set the first row as column headers
    df = df[1:].reset_index()  # Remove the first row and reset the index
    df.rename(columns={'index': 'Header'}, inplace=True)
    df.to_excel(excel_path, index=False,engine='openpyxl')


def add_row_to_excel(json_file, excel_file):
    # Read existing Excel data (if it exists)
    print(f"Reading existing Excel file: {excel_file}")
    if os.path.exists(excel_file):
        df = pd.read_excel(excel_file,engine='openpyxl')
    else:
        with open(json_file) as f:
            sample_data = json.load(f)
        df = pd.DataFrame(columns=sample_data.keys())

    # Load JSON data
    with open(json_file) as f:
        data = json.load(f)
        new_row = {key: value["value"] for key, value in data.items()}

    # Append new row
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # Save back to Excel (preserves existing headers)
    #df = df.transpose()
    df.to_excel(excel_file, index=True, header=True)
    print(f"Added new row to {excel_file} from {json_file}",engine='openpyxl')
