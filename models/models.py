from pydantic import BaseModel

class TemplateCreate(BaseModel):
    name: str
    content: str 
    stage: str
    type: str

class TemplateUpdate(BaseModel):
    name: str | None
    content: str | None
    stage: str | None 
    type: str | None