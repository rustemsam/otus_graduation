from typing import Optional

from pydantic import BaseModel


class CandidateModel(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    email: Optional[str] = None
    date: Optional[str] = None
