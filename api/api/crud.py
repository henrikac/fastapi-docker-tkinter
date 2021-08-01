from sqlalchemy.orm import Session

from . import models, schemas


def get_short_url_by_path(db: Session, path: str):
    return db.query(models.ShortURL).filter(models.ShortURL.path == path).first()


def create_short_url(db: Session, short_url: schemas.ShortURLCreate, path: str):
    db_url = models.ShortURL(url=short_url.url, path=path)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def update_short_url_redirects(db: Session, short_url: schemas.ShortURL):
    short_url.redirects += 1
    db.commit()

