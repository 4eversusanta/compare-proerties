import uuid

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from typing import List, Optional


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)

class SWOTBase(SQLModel):
    category: str = Field(max_length=32, nullable=False)  # E.g., Strength, Weakness
    description: str = Field(nullable=False)

class SWOT(SWOTBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    project_id: uuid.UUID = Field(foreign_key="project.id", nullable=False)

class AmenityBase(SQLModel):
    amenity_name: str = Field(max_length=128, nullable=False)
    description: Optional[str] = Field(nullable=True)

class Amenity(AmenityBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    project_id: uuid.UUID = Field(foreign_key="project.id", nullable=False)

class SWOTPublic(SQLModel):
    category: str
    description: str

class AmenityPublic(SQLModel):
    amenity_name: str
    description: Optional[str]

class DeveloperBase(SQLModel):
    name: str = Field(max_length=128, nullable=False)
    reputation: Optional[str] = Field(max_length=256, nullable=True)  # Optional for nullable fields
    additional_info: Optional[str] = Field(nullable=True)

class Developer(DeveloperBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    projects: List["Project"] = Relationship(
        back_populates="developer",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

class ProjectBase(SQLModel):
    name: str = Field(max_length=128, nullable=False)
    location: Optional[str] = Field(max_length=128, nullable=True)
    latitude: Optional[float] = Field(nullable=True)
    longitude: Optional[float] = Field(nullable=True)
    pricing_range: Optional[str] = Field(max_length=64, nullable=True)
    reraId: Optional[str] = Field(max_length=128, nullable=True)
    description: Optional[str] = Field(nullable=True)
    area: Optional[str] = Field(nullable=True)
    image_url: Optional[str] = Field(max_length=256, nullable=True)
    possession_date: Optional[str] = Field(max_length=64, nullable=True)
    project_type: Optional[str] = Field(max_length=128, nullable=True)
    website: Optional[str] = Field(max_length=256, nullable=True)
    key_amenities: Optional[str] = Field(nullable=True)



class Project(ProjectBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    developer_id: uuid.UUID = Field(foreign_key="developer.id", nullable=False)
    developer: Optional[Developer] = Relationship(back_populates="projects")
    swots: List[SWOT] = Relationship(sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    amenities: List[Amenity] = Relationship(sa_relationship_kwargs={"cascade": "all, delete-orphan"})

class ProjectPublic(ProjectBase):
    id: uuid.UUID
    developer_name: str
    swots: List[SWOTPublic]
    amenities: List[AmenityPublic]

    class Config:
        orm_mode = True

class ProjectsPublic(SQLModel):
    data: List[ProjectPublic]
    count: int

    class Config:
        orm_mode = True