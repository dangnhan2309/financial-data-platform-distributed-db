from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date, datetime


class ConfigORM:
    from_attributes = True  # dùng cho Pydantic v2
class ConfigDict:
    from_attributes = True  # dùng cho Pydantic v2