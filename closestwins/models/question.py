"""Question model module."""

from dataclasses import dataclass


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
