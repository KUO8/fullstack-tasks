from pydantic import BaseModel, Field

def to_camel(string: str) -> str:
    parts = string.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])

class TaskCreate(BaseModel):
    title: str
    completed: bool = False

    model_config = {
        "populate_by_name": True,
        "alias_generator": to_camel
    }

class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
        "alias_generator": to_camel
    }
