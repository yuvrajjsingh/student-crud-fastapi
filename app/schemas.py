"""Request/response validation models."""
from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator


class StudentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100, examples=["Aarav Sharma"])
    date_of_birth: date = Field(examples=["2005-08-17"])
    email: Optional[EmailStr] = Field(default=None, examples=["aarav@example.com"])
    phone: Optional[str] = Field(default=None, min_length=7, max_length=20, examples=["9876543210"])
    course: Optional[str] = Field(default=None, max_length=100, examples=["B.Tech CSE"])
    address: Optional[str] = Field(default=None, max_length=250)
    enrollment_date: Optional[date] = Field(default=None, examples=["2024-08-01"])

    @field_validator("name")
    @classmethod
    def clean_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be blank")
        return value

    @field_validator("date_of_birth")
    @classmethod
    def validate_dob(cls, value: date) -> date:
        if value > date.today():
            raise ValueError("Date of birth cannot be in the future")
        return value

    @model_validator(mode="after")
    def require_contact_method(self):
        if not self.email and not self.phone:
            raise ValueError("Provide at least one contact method: email or phone")
        return self


class StudentUpdate(BaseModel):
    """PATCH model: all fields are optional; only supplied fields are changed."""
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    date_of_birth: Optional[date] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(default=None, min_length=7, max_length=20)
    course: Optional[str] = Field(default=None, max_length=100)
    address: Optional[str] = Field(default=None, max_length=250)
    enrollment_date: Optional[date] = None

    @field_validator("name")
    @classmethod
    def clean_name(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be blank")
        return value

    @field_validator("date_of_birth")
    @classmethod
    def validate_dob(cls, value: Optional[date]) -> Optional[date]:
        if value is not None and value > date.today():
            raise ValueError("Date of birth cannot be in the future")
        return value

    @model_validator(mode="after")
    def require_a_change(self):
        if not self.model_fields_set:
            raise ValueError("Provide at least one field to update")
        if "name" in self.model_fields_set and self.name is None:
            raise ValueError("Name cannot be null")
        if "date_of_birth" in self.model_fields_set and self.date_of_birth is None:
            raise ValueError("Date of birth cannot be null")
        return self


class StudentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    date_of_birth: date
    email: Optional[str] = None
    phone: Optional[str] = None
    course: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[date] = None
    created_at: str
    updated_at: str


class AIQuestion(BaseModel):
    question: str = Field(min_length=3, max_length=500, examples=["How many students are there?"])
