from pydantic import BaseModel

class GetPath(BaseModel):
    path: str

class StatisticsYear(BaseModel):
    year: int