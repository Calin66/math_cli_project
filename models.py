
from pydantic import BaseModel, Field

class PowRequest(BaseModel):
    base: int = Field(..., ge=0)
    exp: int = Field(..., ge=0)

class FibRequest(BaseModel):
    n: int = Field(..., ge=0)

class FactRequest(BaseModel):
    n: int = Field(..., ge=0)
