"""Mock questions service api server."""
import random
from http import HTTPStatus

from flask import Flask, make_response

questions = [
    {
        "question_id": "1",
        "city_name_en": "Santiago",
        "latitude": -33.447487,
        "longitude": -70.673676,
    },
    {
        "question_id": "2",
        "city_name_en": "London",
        "latitude": 51.509865,
        "longitude": -0.118092,
    },
    {
        "question_id": "3",
        "city_name_en": "New York",
        "latitude": 40.730610,
        "longitude": -73.935242,
    },
    {
        "question_id": "4",
        "city_name_en": "Houston",
        "latitude": 29.749907,
        "longitude": -95.358421,
    },
    {
        "question_id": "5",
        "city_name_en": "Cairo",
        "latitude": 30.033333,
        "longitude": 31.233334,
    },
    {
        "question_id": "6",
        "city_name_en": "New Delhi",
        "latitude": 28.644800,
        "longitude": 77.216721,
    },
    {
        "question_id": "7",
        "city_name_en": "Caracas",
        "latitude": 10.500000,
        "longitude": -66.916664,
    },
]

app = Flask(__name__)


@app.route("/question-random", methods=["GET"])
def question_random():
    """Returns a random question."""
    return random.choice(questions)


@app.route("/questions/<question_id>", methods=["GET"])
def get_question(question_id):
    """Returns a question by id."""
    for question in questions:
        if question["question_id"] == question_id:
            return question
    return make_response("not found", HTTPStatus.NOT_FOUND)


if __name__ == "__main__":
    app.run()
