from typing import List, Optional

from pydantic import BaseModel


class Error(BaseModel):
    loc: Optional[List[str]] = None
    msg: str
    type: str


class ErrorResponse(BaseModel):
    detail: List[Error]

