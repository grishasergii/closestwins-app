import random
from http import HTTPStatus

from flask import Flask, make_response

questions = [
    {"id": "1", "city_name": "Santiago", "location": (-33.447487, -70.673676)},
    {"id": "2", "city_name": "London", "location": (51.509865, -0.118092)},
    {"id": "3", "city_name": "New York", "location": (40.730610, -73.935242)},
    {"id": "4", "city_name": "Houston", "location": (29.749907, -95.358421)},
    {"id": "5", "city_name": "Cairo", "location": (30.033333, 31.233334)},
    {"id": "6", "city_name": "New Delhi", "location": (28.644800, 77.216721)},
    {"id": "7", "city_name": "Caracas", "location": (10.500000, -66.916664)},
]

app = Flask(__name__)


@app.route("/question-random", methods=["GET"])
def question_random():
    return random.choice(questions)


@app.route("/questions/<question_id>", methods=["GET"])
def get_question(question_id):
    for question in questions:
        if question["id"] == question_id:
            return question
    return make_response("not found", HTTPStatus.NOT_FOUND)


if __name__ == "__main__":
    app.run(port=5001)
