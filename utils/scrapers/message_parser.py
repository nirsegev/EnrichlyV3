from typing import Dict, Tuple, List
from .models import MessageData, ParsedMessage

def parse_message(data: Dict) -> MessageData:
    """Extract relevant message data."""
    return MessageData(
        chat_id=str(data["message"]["chat"]["id"]),
        first_name=data["message"]["chat"].get("first_name", "User"),
        text=data["message"].get("text")
    )

def extract_tags_from_text(text: str) -> ParsedMessage:
    """Extract tags and link from the text."""
    parts = text.split()
    link = parts[0]
    tags = [part.lstrip("#") for part in parts[1:] if part.startswith("#")]
    return ParsedMessage(link=link, tags=tags) 