import os
import concurrent.futures
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from utils.schemas import TUnitLinkedPlanField
from utils.retrieval_prompts import (
    RETRIEVAL_SYSTEM_PROMPT_1,
    RETRIEVAL_HUMAN_PROMPT_TEMPLATE_3,
    RETRIEVAL_HUMAN_PROMPT_TEMPLATE_2,
)
from utils.retrieval_queries import USER_QUERIES

# Load environment variables
load_dotenv(override=True)

# Constants
DEFAULT_SEARCH_PARAMS = {
    "search_type": "similarity_score_threshold",
    "search_kwargs": {"k": 2, "score_threshold": 0.4},
}
MMR_SEARCH_PARAMS = {
    "search_type": "mmr",
    "search_kwargs": {"k": 3, "fetch_k": 20, "lambda_mult": 0.5},
}
EXAMPLE_DICT = {
    "plan_options": """An example of the output format is given below:
    3 Plan Options
        1) Life Secure: SAD is paid if the Life Assured/Spouse dies during the PT while the policy is in-force;
        2) Life Secure with Income: Monthly Survival Income starts at age 60 and continues until death or end of the PT. If the Life Assured dies, the SAD- paid incomes, is paid and the policy ends;
        3) Life Secure with ROP: SAD is paid if the Life Assured dies and the Policy ends. If the Life Assured survives, the SAM is paid and the Policy ends ;
    """
}


def init_vectorstore(uin: str) -> Chroma:
    """
    Initialize an instance of the existing vector store.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
    db_dir = os.path.join(parent_dir, "neo_db")
    persistent_directory = os.path.join(db_dir, f"chroma_db_{uin}")

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return Chroma(persist_directory=persistent_directory, embedding_function=embeddings)


def retrieve_from_db(db: Chroma, query: str, search_type: str, search_kwargs: dict):
    """
    Retrieve relevant documents from the database.
    """
    retriever = db.as_retriever(search_type=search_type, search_kwargs=search_kwargs)
    return retriever.invoke(query)


def generate_summary(
    relevant_pages, query: str, policy_name: str, field_example: str = ""
) -> TUnitLinkedPlanField:
    """
    Generate a summary for the given query and relevant pages.
    """
    model = ChatOpenAI(model=os.environ.get("MODEL_OPENAI"), temperature=0)

    # Extract page contents
    source_chunks = [page.page_content for page in relevant_pages]
    if not source_chunks:
        return TUnitLinkedPlanField(value="Not Available", chunks=[], page_num="N/A")

    source_chunks_joined = "\n".join(source_chunks)
    user_prompt = RETRIEVAL_HUMAN_PROMPT_TEMPLATE_3.format(
        policy_name=policy_name, source_chunks_joined=source_chunks_joined, query=query
    )

    messages = [
        SystemMessage(content=RETRIEVAL_SYSTEM_PROMPT_1),
        HumanMessage(content=user_prompt),
    ]

    structured_llm = model.with_structured_output(TUnitLinkedPlanField)
    response = structured_llm.invoke(messages)

    # Inject source chunks into the response
    return response.model_copy(update={"chunks": source_chunks})  # type: ignore


def process_query(
    db: Chroma, field: str, query: str, search_params: dict, policy_name: str
):
    """
    Process a single query and return the result with its field name.
    """
    print(f"\n---- Processing query: {field} -----")

    relevant_pages = retrieve_from_db(
        db, query, search_params.get("search_type"), search_params.get("search_kwargs")
    )

    print(f"---- Found {len(relevant_pages)} relevant documents for {field} -----")
    for i, doc in enumerate(relevant_pages, 1):
        print(f"Document {i}:\n{doc.page_content}\n")
        if hasattr(doc, "metadata") and "page" in doc.metadata:
            print(f"Page Number: {doc.metadata['page']}\n")

    result = generate_summary(
        relevant_pages, query, policy_name, EXAMPLE_DICT.get(field, "")
    )
    print(f"Response for {field}: {result}")
    print(f"---------------------------{field} QUERY END----------------------------------------")

    return field, result


def init_retrieval(uin: str, policy_name: str) -> dict:
    """
    Initialize the retrieval process and execute queries in parallel.
    """
    db = init_vectorstore(uin)
    queries = USER_QUERIES

    # Initialize the response dictionary with empty TUnitLinkedPlanField instances
    response = {key: TUnitLinkedPlanField() for key in queries.keys()}

    # Execute queries in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        future_to_field = {
            executor.submit(
                process_query, db, field, query, DEFAULT_SEARCH_PARAMS, policy_name
            ): field
            for field, query in queries.items()
        }

        for future in concurrent.futures.as_completed(future_to_field):
            field, result = future.result()
            response[field] = result

    return response
