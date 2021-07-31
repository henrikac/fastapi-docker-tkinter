import random
import string

from typing import List

from fastapi import Depends, FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from . import crud, errors, models, schemas
from .database import engine, SessionLocal


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
async def add(url: schemas.ShortURLCreate, db: Session = Depends(get_db)):
    path = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    short_url = crud.get_short_url_by_path(db, path)
    if short_url:
        raise HTTPException(status_code=500, detail='Error happened creating the short url')
    return crud.create_short_url(db, url, path)

