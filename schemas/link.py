from typing import List, Dict, Optional
from pydantic import BaseModel

class LinkMetadata(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    price: Optional[str] = None
    images: Optional[List[str]] = None
    site_name: Optional[str] = None

class LinkCreate(BaseModel):
    chat_id: str
    link: str
    tags: List[str]
    metadata: LinkMetadata

class LinkResponse(BaseModel):
    id: int
    message: str 