import os
import concurrent.futures

from dotenv import load_dotenv

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings,ChatOpenAI
from langchain.schema import SystemMessage,HumanMessage

from utils.schemas import TUnitLinkedPlanField
from utils.retrieval_prompts import RETRIEVAL_SYSTEM_PROMPT_1,RETRIEVAL_HUMAN_PROMPT_TEMPLATE_3,RETRIEVAL_SYSTEM_PROMPT_2,RETRIEVAL_HUMAN_PROMPT_TEMPLATE_1,RETRIEVAL_HUMAN_PROMPT_TEMPLATE_2
from utils.retrieval_queries import USER_QUERIES


load_dotenv(override=True)

# initialize an instance of the existing vector store
def init_vectorstore(uin):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, '..','..'))
    db_dir = os.path.join(parent_dir,"neo_db")
    persistent_directory = os.path.join(db_dir, f"chroma_db_{uin}")

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    db = Chroma(persist_directory=persistent_directory, embedding_function=embeddings)

    return db


# Creating this for future extension
def retrieve_from_db(db,query,search_type,search_kwargs):
    retriever = db.as_retriever(
        search_type=search_type,
        search_kwargs=search_kwargs
    )

    return retriever.invoke(query)


def generate_summary(relevant_pages,query,policy_name,field_example="") -> TUnitLinkedPlanField:
    model = ChatOpenAI(model=os.environ.get("MODEL_OPENAI"),temperature=0)

    # Extract page contents from relevant_pages upfront
    source_chunks = [page.page_content for page in relevant_pages] 
    if not source_chunks:
        return TUnitLinkedPlanField(value='Not Available',chunks=[],page_num='N/A')
    
    source_chunks_joined = "\n".join(source_chunks)

    user_prompt_2 = RETRIEVAL_HUMAN_PROMPT_TEMPLATE_2.format(policy_name=policy_name,source_chunks_joined=source_chunks_joined,query=query)
    user_prompt_3 = RETRIEVAL_HUMAN_PROMPT_TEMPLATE_3.format(policy_name=policy_name,source_chunks_joined=source_chunks_joined,query=query)
    
    
    # user_prompt_4 = RETRIEVAL_HUMAN_PROMPT_TEMPLATE_4.format(policy_name=policy_name,documents=source_chunks_joined,query=query)
    

    messages = [
        SystemMessage(content=RETRIEVAL_SYSTEM_PROMPT_1),
        HumanMessage(content=user_prompt_3)
    ]

    structured_llm = model.with_structured_output(TUnitLinkedPlanField)
    response = structured_llm.invoke(messages)
    
    # Manually inject source chunks into the response
    response_with_chunks = response.model_copy(  # Pydantic V2 syntax
        update={"chunks": source_chunks}
    )
    
    return response_with_chunks #type: ignore


example_dict = {
    "plan_options" : """An example of the output format is given below:
    3 Plan Options
        1) Life Secure: SAD is paid if the Life Assured/Spouse dies during the PT while the policy is in-force;
        2) Life Secure with Income: Monthly Survival Income starts at age 60 and continues until death or end of the PT. If the Life Assured dies, the SAD- paid incomes, is paid and the policy ends;
        3) Life Secure with ROP: SAD is paid if the Life Assured dies and the Policy ends. If the Life Assured survives, the SAM is paid and the Policy ends ;
    """
}
def process_query(db, field, query, search_params,policy_name):
    """
    Process a single query and return the result with its field name
    """
    print(f"\n---- Processing query: {field} -----")
    

    relevant_pages = retrieve_from_db(db, query, search_params.get('search_type'), search_params.get('search_kwargs'))
    
    print(f"---- Found {len(relevant_pages)} relevant documents for {field} -----")
    for i, doc in enumerate(relevant_pages, 1):
        print(f"Document {i}:\n{doc.page_content}\n")
        if hasattr(doc, 'metadata') and 'page' in doc.metadata:
            print(f"Page Number: {doc.metadata['page']}\n")
    
    result = generate_summary(relevant_pages, query,policy_name, example_dict.get(field, ""))
    print(f"Response for {field}: {result}")
    print(f"---------------------------{field} QUERY END----------------------------------------")
    
    return field, result



def init_retrieval(uin,policy_name):
    
    db = init_vectorstore(uin)

    queries = USER_QUERIES

    
    # Default search parameters - can be customized per query if needed
    search_params = {
        "search_type": "similarity_score_threshold",
        "search_kwargs": {"k": 3, "score_threshold": 0.4}
    }

    search_params_mmr = {
        "search_type": "mmr",
        "search_kwargs": {"k": 3, "fetch_k": 20, "lambda_mult": 0.5}
    }

    retriever = db.as_retriever(
        search_type=search_params["search_type"],
        search_kwargs=search_params["search_kwargs"]
    )
    # print(db._persist_directory)
    # result = retriever.invoke("What are the plan options available for this policy? Give brief description of each plan option.")
    # print("---------------RESPONSE-----------",result)

    # Initialize the response dictionary with empty TUnitLinkedPlanField instances     
    response = {key: TUnitLinkedPlanField() for key in queries.keys()}
    
    # Execute queries in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        # Submit all tasks
        future_to_field = {
            executor.submit(process_query, db, field, query, search_params,policy_name): field
            for field, query in queries.items()
        }
        
        # Collect results as they complete
        for future in concurrent.futures.as_completed(future_to_field):
            field, result = future.result()
            response[field] = result



    return response
