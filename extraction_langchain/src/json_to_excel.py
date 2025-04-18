import json
import os
import pandas as pd
import sys 


# Path to directory containing JSON files
json_dir = '../neo_extracted_data'
# Path to output Excel file
excel_path = '../results_second.xlsx'

def add_rows_to_excel(json_dir, excel_path):
    # Check if the directory exists
    print("Checking if the directory exists...")
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
    headers = df.iloc[0].tolist()

    # Extract the data (excluding the header row)
    data = df.iloc[1:, 1:]

    # Transpose the data
    transposed_df = data.transpose()

    # Set the first column as headers
    transposed_df.columns = df.iloc[:, 0].tolist()[1:]  # Skip the first empty header

    # The original headers become the first column
    transposed_df.insert(0, headers[0], headers[1:])

    # Save the transposed data to a new Excel file
    transposed_df.to_excel(excel_path, index=False, engine='openpyxl')

def add_row_to_excel(json_file, excel_file):
    # Read existing Excel data (if it exists)
    print(f"Reading existing Excel file: {excel_file}")
    if os.path.exists(excel_file):
            if os.path.getsize(excel_file) == 0:
                # Handle empty file case
                df = pd.DataFrame()
            else:
                if os.path.exists(excel_file):
                    df = pd.read_excel(excel_file, engine='openpyxl')
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
    df.to_excel(excel_file, index=True, header=True,engine='openpyxl')
    print(f"Added new row to {excel_file} from {json_file}")

def main():
    # Example usage
    if sys.argv[1] == '1':
        # Add all JSON files in the directory to the Excel file
        print("Adding all JSON files to the Excel file...")
        add_rows_to_excel(json_dir, excel_path)
    elif sys.argv[1] == '2':
        # Add a single JSON file to the Excel file
        uin = sys.argv[2]
        json_file = f'./neo_extracted_data/{uin}_rag.json'
        add_row_to_excel(json_file, excel_path)

if __name__ == "__main__":
    main()  