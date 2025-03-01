from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import UserLink, Tag

async def save_link_to_db(
    db: Session,
    chat_id: str,
    link: str,
    tags: List[str],
    metadata: Dict[str, Optional[str]]
) -> int:
    """
    Save link and metadata to the database.
    
    Args:
        db: Database session
        chat_id: Telegram chat ID
        link: URL to save
        tags: List of tag names
        metadata: Dictionary containing link metadata
        
    Returns:
        int: ID of the saved link
        
    Raises:
        HTTPException: If database operation fails
    """
    print("Saving link to database")
    try:
        # Create UserLink instance
        user_link = UserLink(
            chat_id=chat_id,
            link=link,
            title=metadata.get("title"),
            description=metadata.get("description"),
            url=metadata.get("url"),
            price=metadata.get("price"),
            images=metadata.get("images"),
            site_name=metadata.get("site_name"),
        )

        # Process tags
        for tag_name in tags:
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.add(tag)
            user_link.tags.append(tag)

        db.add(user_link)
        db.commit()
        db.refresh(user_link)
        
        print(f"Link saved with ID: {user_link.id}")
        return user_link.id
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save link to database: {str(e)}"
        )

async def add_tag_to_link(
    db: Session,
    link_id: int,
    tag_name: str
) -> None:
    """
    Add a tag to a specific link.
    
    Args:
        db: Database session
        link_id: ID of the link
        tag_name: Name of the tag to add
        
    Raises:
        HTTPException: If link not found or operation fails
    """
    try:
        link = db.query(UserLink).get(link_id)
        if not link:
            raise HTTPException(
                status_code=404,
                detail=f"Link with ID {link_id} not found"
            )

        tag = db.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            db.add(tag)

        if tag not in link.tags:
            link.tags.append(tag)
            db.commit()
            
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to add tag to link: {str(e)}"
        ) 