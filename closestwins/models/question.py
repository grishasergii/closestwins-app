"""Question model module."""

from dataclasses import dataclass
from typing import List


@dataclass
class Question:
    """Question model."""

    question_id: str
    city_name_en: str
    latitude: float
    longitude: float

    @property
    def city_name(self):
        """City name property."""
        return self.city_name_en

    @property
    def lat(self):
        """Latitude property."""
        return self.latitude

    @property
    def lng(self):
        """Longitude property."""
        return self.longitude


@dataclass
class RoomSettings:
    """Room settings model."""
    number_of_questions: int
    round_duration_seconds: int


@dataclass
class Room:
    """Room model."""
    room_id: str
    settings: RoomSettings
    current_question_index: int
    status: str
    question_ids: List[str]

    def __post_init__(self):
        if isinstance(self.settings, dict):
            self.settings = RoomSettings(**self.settings)
