from pydantic import BaseModel


class RootResponse(BaseModel):
    status: str
    name: str
    version: str
    description: str
    authors: list
    running_mode: str

    class Config:
        from_attributes = True
