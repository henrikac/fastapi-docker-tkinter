import random
import string

from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session

from . import crud, errors, models, schemas
from .database import engine, SessionLocal


PATH_LENGTH = 6


models.Base.metadata.create_all(bind=engine)


app = FastAPI(title='URL Shortener API', description='A url shortener api',
    responses={status.HTTP_400_BAD_REQUEST: {'model': errors.ErrorResponse}}
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({'detail': exc.errors()})
    )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/', response_model=schemas.ShortURL)
async def add_short_url(url: schemas.ShortURLCreate, db: Session = Depends(get_db)):
    path = ''.join(random.choices(
        string.ascii_letters + string.digits,
        k=PATH_LENGTH
    ))
    short_url = crud.get_short_url_by_path(db, path)
    if short_url:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error happened creating the short url'
        )
    return crud.create_short_url(db, url, path)


@app.get('/urls', response_model=List[schemas.ShortURL])
async def get_all_urls(db: Session = Depends(get_db)):
    return crud.get_short_urls(db)


@app.get('/{path}')
async def redirect_to_path(path: str, db: Session = Depends(get_db)):
    if len(path) != PATH_LENGTH:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='invalid short url'
        )
    short_url = crud.get_short_url_by_path(db, path)
    if not short_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='unknown short url'
        )
    crud.update_short_url_redirects(db, short_url)
    return RedirectResponse(url=short_url.url)

