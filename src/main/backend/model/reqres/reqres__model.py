from typing import List, Optional
from pydantic import BaseModel, Field


class ResourceResponse(BaseModel):
    """Model for a single resource item."""

    id: int
    name: str
    year: int
    color: str
    pantone_value: str


class UserResponse(BaseModel):
    """Model for a single user item."""

    id: int
    email: str
    first_name: str
    last_name: str
    avatar: str


class ResourceSupportResponse(BaseModel):
    """Model for support information associated with resources or users."""

    url: str
    text: str


class ReqResResourcesResponse(BaseModel):
    """Response model for a list of resources."""

    page: int
    per_page: int
    total: int
    total_pages: int
    data: List[ResourceResponse]
    support: ResourceSupportResponse


class ReqResUsersResponse(BaseModel):
    """Response model for a list of users."""

    page: int
    per_page: int
    total: int
    total_pages: int
    data: List[UserResponse]
    support: ResourceSupportResponse


class ReqResUserResponse(BaseModel):
    """Response model for a single user."""

    data: UserResponse
    support: ResourceSupportResponse


class ReqResResourceResponse(BaseModel):
    """Response model for a single resource."""

    data: ResourceResponse
    support: ResourceSupportResponse


class ReqResUpdateResponse(BaseModel):
    """Response model for update operations."""

    updatedAt: str = Field()

    class Config:
        allow_population_by_field_name = True


class UserRequestBody(BaseModel):
    """Request model for creating or updating a user."""

    name: str
    job: str


class RegisterRequestBody(BaseModel):
    """Request model for user registration."""

    email: Optional[str]
    password: Optional[str] = None


class RegisterResponseBody(BaseModel):
    """Response model for a successful user registration."""

    id: int
    token: str


class LoginResponseBody(BaseModel):
    """Response model for a successful user login."""

    token: str


class RegisterErrorResponse(BaseModel):
    """Response model for registration errors."""

    error: str


class UserResponseBody(BaseModel):
    """Response model for a created user."""

    name: str
    job: str
    id: str
    createdAt: str = Field()

    model_config = {"allow_population_by_field_name": True}
