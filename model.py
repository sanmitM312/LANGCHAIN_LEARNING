from langchain_openai import ChatOpenAI
from langchain.chat_models import init_chat_model
from langchain.schema import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


import os
import getpass
from typing import Optional
from pydantic import BaseModel, Field

from dotenv import load_dotenv

from schemas.Person import Person
from schemas.PersonData import PersonData

prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert extraction algorithm. "
            "Only extract relevant information from the text. "
            "If you do not know the value of an attribute asked to extract, "
            "return null for the attribute's value.",
        ),
        # Please see the how-to about improving performance with
        # reference examples.
        # MessagesPlaceholder('examples'),
        ("human", "{text}"),
    ]
)



def get_llm_response(prompt):
    try:
        load_dotenv()
        if not os.getenv("OPENAI_API_KEY"):
            os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")
        
        openai_api_key = os.getenv("OPENAI_API_KEY")
        llm = ChatOpenAI(model_name='gpt-4o-mini')
        structured_llm = llm.with_structured_output(schema=PersonData)
        
        return structured_llm.invoke(prompt)

    except ValueError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"An error occurred: {e}"
def main():


    singleInfo = "Alan Smith is a 6 feet person tall and has blond hair."
    multipleInfo = "My name is Jeff, my hair is black and i am 6 feet tall. Anna has the same color hair as me."
    prompt = prompt_template.invoke({"text" : multipleInfo})
    response = get_llm_response(prompt)

    if response is not None:
       print(response)
    else:
        print("ggpp")
if __name__ == '__main__':
    main()