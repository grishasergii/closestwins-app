from dataclasses import dataclass


@dataclass
class Question:
    id: str
    city_name: str
    location: (float, float)

    @property
    def lat(self):
        return self.location[0]

    @property
    def lng(self):
        return self.location[1]
