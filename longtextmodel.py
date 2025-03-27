from io import BytesIO
import streamlit as st
import re
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.chat_models import init_chat_model
from langchain.prompts import ChatPromptTemplate
from utils.classes import TUnitLinkedPlan
from dotenv import load_dotenv
import os
import getpass
from langchain_text_splitters import TokenTextSplitter
from typing import List

# extract a pdf using langchain -- done
# map it to TUnitLinkedPlan using longtext reader -- done
# evaluation metric keep it using OpenAI itself


def extract_from_pdf_v2(pdf_file) -> str:
    loader = PyMuPDFLoader(pdf_file)
    documents = loader.load()
    pdf_text = ""
    for doc in documents:
        pdf_text += doc.page_content + "\n"
    st.text_area("Extracted Text", pdf_text,height=400)

    return documents[0]

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


def main():
    st.title("Policy Extractor")
    st.write("Data Extraction From Policy Documents made easy")

    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    if uploaded_file:
        st.write("Processing your file....")
        temp_file = "./temp.pdf"

        with open(temp_file, "wb") as file:
            file.write(uploaded_file.getvalue())
            file_name = file.name
        

        # PDF extraction from text
        pdf_content = extract_from_pdf_v2(temp_file)
        print(pdf_content)
        # st.write("Extracted Text", pdf_content, height=200)


        try:
            load_dotenv()
            if not os.getenv("OPENAI_API_KEY"):
                os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

        
            system_prompt = """
                You are a insurance policy document analysis expert with a focus on extracting, organizing, and presenting structured and comprehensive information from policy documents. 
                Your task is to extract detailed numerical and descriptive insights about a unit-linked policy from the given document. 
                Ensure the output is precise, complete, and strictly adheres to the format outlined below. Do not generate or hallucinate data. 
                Only extract information explicitly stated in the document.

                ### Structure of Extracted Features:
                1. Company:
                2. Product Name:
                3. Product Type:
                4. Product UIN:
                5. Plan Description:
                6. Key Features:
                7. Plan Options:
                8. Premium Payment Option:
                9. Min Age at Entry (in Years):
                10. Max Age at Entry (in Years):
                11. Max Age at Maturity (in Years):
                12. Minimum Sum Assured (in INR):
                13. Maximum Sum Assured (in INR):
                14. Minimum Policy Term (in Years):
                15. Maximum Policy Term (in Years):
                16. Premium Paying Term (in Years):
                17. Annual Minimum Premium (in INR):
                18. Maximum Premium (in INR):
                19. Minimum Top-Up Premium (in INR):
                20. Maximum Top-Up Premium (in INR):

                ### Instructions:

                #### 1. **Strict Extraction**:
                - Extract details strictly as stated in the document. Do not generate or infer data unless explicitly mentioned.
                - If a feature is not explicitly mentioned, write "Not Specified."
                - For every field, specify the **page number** where the information was extracted.

                #### 2. **Statistical Insights for Comparison**:
                - Provide additional statistical information to enable comparisons between policy documents. For instance:
                - Charges and benefits across the policy term (e.g., "Policy Admin Charge: ₹200/month, totaling ₹2,400 annually").
                - Premium breakdowns for different premium-paying terms (e.g., "Annual Premium: ₹50,000 for Limited Pay 5 years, ₹30,000 for others").
                - Fund performance or loyalty additions (e.g., "Loyalty additions of 1.8% of fund value starting from the 10th policy year").
                - Partial withdrawal limits (e.g., "Maximum of 4 withdrawals per year, with a ₹100 charge for additional withdrawals").
                - Surrender charges or penalties where applicable.

                #### 3. **Format Consistency**:
                - Use consistent formatting for clarity:
                - Ages and terms as whole numbers (e.g., "30 years").
                - Monetary values in INR format with commas (e.g., "₹50,000").
                - Percentages for benefits and charges (e.g., "1.8% loyalty additions").
                - Present multi-line features like Key Features and Plan Options as bullet points or numbered lists.

                #### 4. **Example Output**:
                Use the following format for extracted features:

                1. Company: 
                    - Value: HDFC Life
                    - Page Number: 1
                2. Product Name: 
                    - Value: HDFC Life Smart Protect Plan
                    - Page Number: 1
                3. Product Type: 
                    - Value: Unit Linked Plan
                    - Page Number: 2
                4. Product UIN: 
                    - Value: 101L175V03
                    - Page Number: 2
                5. Plan Description: 
                    - Value: Unit Linked Plan offering high death benefits and multiple investment options.
                    - Page Number: 3
                6. Key Features: 
                    - Value:
                        - Comprehensive risk coverage with investment flexibility.
                        - Loyalty additions and fund boosters starting from the 10th policy year.
                        - Multiple premium payment options with customizable payment terms.
                        - Capital guarantee features and systematic transfer strategies.
                        - Tax benefits under prevailing laws.
                    - Page Number: 3
                (Continue similarly for all fields...)

                #### 5. **Traceability**:
                - Always include the **page number** for every extracted field to ensure traceability of information.

                #### 6. **Error Handling**:
                - In case of missing, ambiguous, or conflicting data, mark the feature as "Not Specified" and do not attempt to infer or fill in the gaps.
            """

            prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", system_prompt),
                    ("human", "{text}"),
                ]
            )
            llm = init_chat_model(
                    "gpt-4o",
                    model_provider="openai",
                    temperature=0,
                    max_tokens=1200,
                )

        except Exception as e:
            st.error(f"Error: {e}")
            
        # # Use the LLM to extract structured data
        extractor = prompt | llm.with_structured_output(
            schema=TUnitLinkedPlan,
            include_raw=False
        )

        # print(extractor)

        text_splitter = TokenTextSplitter(
            # Controls the size of each chunk
            chunk_size=2000,
            # Controls overlap between chunks
            chunk_overlap=20,
        )

        # Batch processing
        texts = text_splitter.split_text(pdf_content.page_content)
        first_few = texts[:3]

        extractions = extractor.batch(
            [{"text": text} for text in first_few],
            {"max_concurrency": 5},  # limit the concurrency by passing max concurrency!
        )

        print(isinstance(extractions[0],TUnitLinkedPlan)) # True

        policy_details = extractions[0]
        st.warning("Ground truth data not available. Accuracy scores will be shown as N/A.")
        table = merge_policy_and_accuracy_tables(policy_details, {})
        st.subheader("Policy Details")
        st.table(table)
       
if __name__ == '__main__':
    main()