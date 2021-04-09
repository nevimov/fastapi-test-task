from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class ShortUrl(Base):
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, server_default=func.clock_timestamp())

    key = Column(String(20), index=True, unique=True)
    # The key is a part of the short URL after the domain and slash.
    # For example, given the URL 'shurl.me/foo-bar', the key would be 'foo-bar'.

    destination = Column(String(2048), index=True)
    # The full, original URL.

    owner_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    owner = relationship("User", back_populates="urls")
