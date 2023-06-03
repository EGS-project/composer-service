'''response schemas '''

from typing import Optional
from pydantic import BaseModel


class Conversion(BaseModel):
    format: str
    size: Optional[int]
    target_format: str

    
class ConversionCreate(Conversion):
    pass

class ConversionRead(Conversion):
    link: str
