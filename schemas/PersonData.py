from schemas.Person import Person
from typing import List
from pydantic import BaseModel

class PersonData(BaseModel):
    """Extracted data about people."""

    # Creates a model so that we can extract multiple entities.
    people: List[Person]