from typing import Optional
from pydantic import BaseModel, Field

class Person(BaseModel):
    name : Optional[str] = Field(default=None, description="The name of the person")
    height_in_meters: Optional[str] = Field(
        default=None, description="Height measure in meters"
    )
