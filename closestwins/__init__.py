"""Closest wins application."""

import json
import os

from flask import Flask, render_template, request
from geopy import distance

from closestwins.api.api import QuestionsApi


def create_app():
    """Creates a flask app."""
    app = Flask(__name__)
    app.jinja_env.globals.update(  # pylint: disable=no-member
        MAP_API_KEY=os.environ["MAP_API_KEY"]
    )

    questions_api = QuestionsApi(os.environ["API_ENDPOINT"], os.environ["AWS_REGION"])

    @app.route("/")
    def question_page():
        question = questions_api.get_random_question()
        return render_template(
            "question.html",
            city_name=question.city_name,
            question_id=question.question_id,
        )

    @app.route("/answer", methods=["POST"])
    def answer_page():
        answer = json.loads(request.form.get("answer", "not found"))
        question = questions_api.get_question(answer["question_id"])

        city_name = answer["city_name"]
        lat = answer["lat"]
        lng = answer["lng"]

        lat_true = question.lat
        lng_true = question.lng

        distance_object = distance.distance((lat, lng), (lat_true, lng_true))
        distance_presentation = f"{distance_object.km:.0f} km"

        if distance_object.km < 1:
            distance_presentation = f"{distance_object.m:.0f} m"

        return render_template(
            "answer.html",
            lat_answer=lat,
            lng_answer=lng,
            lat_true=lat_true,
            lng_true=lng_true,
            distance=distance_presentation,
            city_name=city_name,
        )

    return app
