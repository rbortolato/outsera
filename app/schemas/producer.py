"""Pydantic response schemas."""

from typing import List

from pydantic import BaseModel, Field


class ProducerInterval(BaseModel):
    producer: str
    interval: int
    previous_win: int = Field(..., alias="previousWin")
    following_win: int = Field(..., alias="followingWin")

    class Config:
        allow_population_by_field_name = True


class ProducerIntervalsResponse(BaseModel):
    min: List[ProducerInterval]
    max: List[ProducerInterval]
