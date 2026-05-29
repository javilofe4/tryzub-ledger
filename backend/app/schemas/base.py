from datetime import datetime
from enum import Enum

from pydantic import BaseModel, field_validator


class BaseConfigModel(BaseModel):
    model_config = {"from_attributes": True}

    @field_validator("*", mode="before")
    @classmethod
    def serialize_enum_values(cls, value):
        if isinstance(value, Enum):
            return value.value
        return value


class TimestampedModel(BaseConfigModel):
    created_at: datetime | None = None
    updated_at: datetime | None = None
