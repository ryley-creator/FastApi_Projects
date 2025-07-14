from sqlalchemy import Column, Integer, String, Text
from database import Base


class MarkdownFile(Base):
    __tablename__ = "markdown_files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), unique=True, nullable=False)
    note = Column(Text, nullable=False)