from pydantic import BaseModel

class JournalCreate(BaseModel):
    content: str


class JournalResponse(BaseModel):
    id: int
    content: str
    emotion: str

    class Config:
        orm_mode = True