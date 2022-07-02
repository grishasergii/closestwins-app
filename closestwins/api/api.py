"""REST Api wrapper."""
import json

from generic_api_wrapper import Api, AwsIamAuth

from closestwins.models.question import Question, Room


class ClosestwinsApi:
    """Closestwins REST API wrapper."""

    def __init__(self, base_url):
        self.api = Api(base_url, AwsIamAuth(base_url).auth)

    def get_random_question(self):
        """Returns a random question."""
        response = self.api["question-random"]()
        return Question(**response)

    def get_question(self, question_id):
        """Returns a question by its id."""
        response = self.api.questions[question_id]()
        return Question(**response)

    def get_room(self, room_id):
        """Returns a question by its id."""
        response = self.api.rooms[room_id]()
        return Room(**response)

    def create_room(self, room_settings):
        """Create a multiplayer room."""
        response = self.api.rooms.post(data=json.dumps(room_settings))
        return response["room_id"]

    def save_answer(self, question_id, latitude, longitude):
        """Save an answer to a question."""
        return self.api.answers.post(
            json={
                "question_id": question_id,
                "latitude": latitude,
                "longitude": longitude,
            }
        )
