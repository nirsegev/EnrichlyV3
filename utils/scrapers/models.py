from typing import List, Optional
from pydantic import BaseModel

class ProductData(BaseModel):
    title: str
    description: Optional[str] = None
    images: List[str]
    price: Optional[str] = None
    url: str
    site_name: Optional[str] = None

class MessageData(BaseModel):
    chat_id: str
    first_name: str
    text: Optional[str] = None

class ParsedMessage(BaseModel):
    link: str
    tags: List[str] 