from pydantic import BaseModel

class StringCreate(BaseModel):
    value: str
