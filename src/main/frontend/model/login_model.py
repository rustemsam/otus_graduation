from typing import Optional

from pydantic import BaseModel


class LoginModel(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
