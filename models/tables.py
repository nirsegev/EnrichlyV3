from sqlalchemy import Table, Column, Integer, ForeignKey, Index
from .base import Base

# Association tables
link_tags = Table(
    "link_tags",
    Base.metadata,
    Column(
        "link_id",
        Integer,
        ForeignKey("user_links.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tag_id",
        Integer,
        ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Index("ix_link_tags_link_tag", "link_id", "tag_id"),  # Composite index
)

file_tags = Table(
    "file_tags",
    Base.metadata,
    Column(
        "file_id",
        Integer,
        ForeignKey("user_files.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tag_id",
        Integer,
        ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Index("ix_file_tags_file_tag", "file_id", "tag_id"),  # Composite index
)

note_tags = Table(
    "note_tags",
    Base.metadata,
    Column(
        "note_id",
        Integer,
        ForeignKey("user_notes.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tag_id",
        Integer,
        ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Index("ix_note_tags_note_tag", "note_id", "tag_id"),  # Composite index
) 