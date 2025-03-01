from typing import Optional

from pydantic import BaseModel


class PimEmployeeModel(BaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    confirm_password: Optional[str] = None
