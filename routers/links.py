from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import get_db
from services import save_link_to_db, add_tag_to_link
from schemas.link import LinkCreate, LinkResponse

router = APIRouter()

@router.post("/links/", response_model=LinkResponse)
async def create_link(
    link_data: LinkCreate,
    db: Session = Depends(get_db)
):
    """Create a new link with tags."""
    link_id = await save_link_to_db(
        db,
        link_data.chat_id,
        link_data.link,
        link_data.tags,
        link_data.metadata
    )
    return {"id": link_id, "message": "Link saved successfully"}

@router.post("/links/{link_id}/tags/{tag_name}")
async def add_tag(
    link_id: int,
    tag_name: str,
    db: Session = Depends(get_db)
):
    """Add a tag to an existing link."""
    await add_tag_to_link(db, link_id, tag_name)
    return {"message": "Tag added successfully"} 