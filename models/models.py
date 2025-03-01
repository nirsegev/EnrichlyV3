from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base
from .tables import link_tags, file_tags, note_tags

class UserLink(Base):
    __tablename__ = "user_links"

    id = Column(Integer, primary_key=True)
    chat_id = Column(String, nullable=False, index=True)  # Telegram chat ID
    link = Column(String, nullable=False)
    title = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    url = Column(String, nullable=True)
    price = Column(String, nullable=True)
    images = Column(JSON, nullable=True)  # Store as JSON
    site_name = Column(String, nullable=True)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    tags = relationship("Tag", secondary=link_tags, back_populates="links")
    notes = relationship(
        "UserNote",
        backref="link",
        lazy="joined",
        cascade="all, delete",  # Deletes associated UserNotes when UserLink is deleted
    )

    def __repr__(self):
        return f"<UserLink {self.title}>"


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True, index=True)

    links = relationship("UserLink", secondary=link_tags, back_populates="tags")
    files = relationship("UserFile", secondary=file_tags, back_populates="tags")
    notes = relationship("UserNote", secondary=note_tags, back_populates="tags")

    def __repr__(self):
        return f"<Tag {self.name}>"


class UserFile(Base):
    __tablename__ = "user_files"

    id = Column(Integer, primary_key=True)
    chat_id = Column(String, nullable=False, index=True)  # Telegram chat ID
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)  # Path where the file is stored
    summary = Column(Text, nullable=True)  # AI-generated summary of the file
    title = Column(String, nullable=True)  # Optional title for the file
    thumbnail_image = Column(String, nullable=True)  # Path to the thumbnail image
    extracted_text = Column(Text, nullable=True)  # Optional extracted text from the file
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    tags = relationship("Tag", secondary=file_tags, back_populates="files")
    notes = relationship(
        "UserNote",
        backref="file",
        lazy="joined",
        cascade="all, delete",  # Deletes associated UserNotes when UserFile is deleted
    )

    def __repr__(self):
        return f"<UserFile {self.file_name}>"


class UserNote(Base):
    __tablename__ = "user_notes"

    id = Column(Integer, primary_key=True)
    file_id = Column(
        Integer, ForeignKey("user_files.id"), nullable=True, index=True
    )  # Reference to UserFile (optional)
    link_id = Column(
        Integer, ForeignKey("user_links.id"), nullable=True, index=True
    )  # Reference to UserLink (optional)
    chat_id = Column(String, nullable=False, index=True)  # Telegram chat ID
    note_content = Column(Text, nullable=False)  # User's note content
    note_title = Column(String, nullable=True)  # Optional title for the note
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    tags = relationship("Tag", secondary=note_tags, back_populates="notes")

    def __repr__(self):
        return f"<UserNote {self.id}>" 