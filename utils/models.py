from typing import List
from pydantic import BaseModel

class Recommendation(BaseModel):
    destination_tag: str
    title: str
    link: str

class UserAnalysis(BaseModel):
    general: str
    recommendations: List[Recommendation] 