from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from models import get_db
from services.management_service import (
    create_database_tables,
    list_html_files,
    summarize_user_links,
    generate_summary_cards,
    delete_all_user_data
)

router = APIRouter(prefix="/management", tags=["management"])

@router.get("/create_db")
async def create_db(db: Session = Depends(get_db)):
    """Create all database tables."""
    return await create_database_tables(db)

@router.get("/list_html_files", response_model=List[str])
async def list_files():
    """List all HTML files in storage."""
    return await list_html_files()

@router.get("/summarize_links/{chat_id}")
async def summarize_links(chat_id: str, db: Session = Depends(get_db)):
    """Generate AI summary of user's links."""
    return await summarize_user_links(chat_id)

@router.get("/generate_summary_cards/{chat_id}")
async def generate_cards(chat_id: str):
    """Generate HTML cards from summary."""
    return await generate_summary_cards(chat_id)

@router.delete("/delete_all/{chat_id}")
async def delete_all(chat_id: str, db: Session = Depends(get_db)):
    """Delete all user data."""
    return await delete_all_user_data(db, chat_id) 