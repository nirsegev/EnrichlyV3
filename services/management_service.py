import os
import json
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException
import openai
from models import UserLink, Tag
from config import get_settings
from utils import generate_html

settings = get_settings()

async def create_database_tables(db: Session):
    """Create all database tables."""
    try:
        # SQLAlchemy will create tables based on models
        from models.base import Base
        Base.metadata.create_all(bind=db.get_bind())
        return "All database tables created successfully!"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def list_html_files() -> List[str]:
    """List all HTML files in the links history directory."""
    try:
        files = os.listdir(str(settings.LINKS_HISTORY_PATH))
        return [f for f in files if f.endswith(".html")]
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="The specified directory does not exist.")

async def summarize_user_links(chat_id: str) -> str:
    """Generate AI summary of user's links."""
    try:
        # Retrieve user links from the database
        user_links = (
            db.query(UserLink)
            .filter_by(chat_id=chat_id)
            .order_by(UserLink.created_at)
            .all()
        )
        
        if not user_links:
            raise HTTPException(status_code=404, detail="No links found for this user.")

        # Format links for the prompt
        formatted_links = [
            {
                "title": link.title,
                "description": link.description,
                "tags": [tag.name for tag in link.tags],
                "created_at": link.created_at.strftime("%Y-%m-%d"),
            }
            for link in user_links
        ]

        # Construct prompts
        system_prompt = "You are a marketing strategist..."  # Your existing system prompt
        user_prompt = f"Based on the user's saved data..." # Your existing user prompt

        # Send to OpenAI
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

        analysis = response.choices[0].message.content.strip()

        # Save analysis
        file_name = f"{chat_id}_summary.json"
        file_path = os.path.join(str(settings.LINKS_HISTORY_PATH), file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "w") as file:
            file.write(analysis)

        return analysis

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def generate_summary_cards(chat_id: str) -> Dict[str, str]:
    """Generate HTML cards from summary JSON."""
    try:
        summary_file_path = os.path.join(str(settings.LINKS_HISTORY_PATH), f"{chat_id}_summary.json")
        
        if not os.path.exists(summary_file_path):
            raise HTTPException(status_code=404, detail=f"Summary file for chat_id {chat_id} not found.")

        with open(summary_file_path, "r") as summary_file:
            summary_data = json.load(summary_file)

        # Your existing HTML generation code...
        cards_html = ""
        for recommendation in summary_data.get("recommendations", []):
            # Your existing card generation code...
            pass

        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <!-- Your existing HTML template -->
        </html>
        """

        output_file_path = os.path.join(str(settings.LINKS_HISTORY_PATH), f"summary_cards_{chat_id}.html")
        with open(output_file_path, "w") as output_file:
            output_file.write(html_content)

        return {"message": "HTML generated successfully.", "html_file": output_file_path}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def delete_all_user_data(db: Session, chat_id: str) -> Dict[str, str]:
    """Delete all links and tags for a user."""
    try:
        links = db.query(UserLink).filter_by(chat_id=chat_id).all()
        if not links:
            raise HTTPException(status_code=404, detail="No links found for this chat ID")

        # Delete links
        for link in links:
            db.delete(link)

        # Delete unused tags
        unused_tags = db.query(Tag).filter(~Tag.links.any()).all()
        for tag in unused_tags:
            db.delete(tag)

        db.commit()

        # Regenerate empty HTML
        await generate_html(chat_id, [], [], [], "User")

        return {"message": "All links and tags deleted successfully!"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e)) 