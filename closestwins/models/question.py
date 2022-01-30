"""Question model module."""

from dataclasses import dataclass


@dataclass
class Question:
    """Question model."""

    id: str
    city_name: str
    location: (float, float)

    @property
    def lat(self):
        """Latitude property."""
        return self.location[0]

    @property
    def lng(self):
        """Longitude property."""
        return self.location[1]
