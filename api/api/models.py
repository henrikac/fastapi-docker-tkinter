from sqlalchemy import Column, Integer, String

from .database import Base


class ShortURL(Base):
    __tablename__ = 'short_urls'

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    path = Column(String, unique=True, index=True)
    redirects = Column(Integer, default=0)

