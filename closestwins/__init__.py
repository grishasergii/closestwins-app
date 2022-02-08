"""Closest wins application."""

import json
import os

from flask import Flask, render_template, request, abort, url_for
from geopy import distance

from closestwins.api.api import ClosestwinsApi
from werkzeug.exceptions import HTTPException


def create_app():
    """Creates a flask app."""
    app = Flask(__name__)
    app.config["TRAP_HTTP_EXCEPTION"] = True
    app.jinja_env.globals.update(  # pylint: disable=no-member
        MAP_API_KEY=os.environ["MAP_API_KEY"]
    )

    closestwins_api = ClosestwinsApi(
        os.environ["REST_API_ENDPOINT"], os.environ["AWS_REGION"]
    )

    @app.route("/")
    def question_page():
        question = closestwins_api.get_random_question()
        return render_template(
            "question_single_player.html",
            city_name=question.city_name,
            question_id=question.question_id,
        )

    @app.route("/create-multiplayer-room", methods=["GET", "POST"])
    def create_multiplayer_room():
        if request.method == "GET":
            return render_template("create_multiplayer_room.html")

        form_data = request.form
        if not form_data:
            abort(500)

        room_settings = {
            "settings": {
                "number_of_questions": int(form_data["number_of_questions"]),
                "round_duration_seconds": int(form_data["round_duration_seconds"]),
            }
        }

        room_id = closestwins_api.create_room(room_settings)

        return render_template(
            "lobby.html",
            room_id=room_id,
            websocket_url=os.environ["WEBSOCKET_URL"],
            is_owner=True,
            invite_link=url_for("lobby", room_id=room_id, _external=True),
        )

    @app.route("/lobby/<room_id>")
    def lobby(room_id):
        return render_template(
            "lobby.html",
            room_id=room_id,
            websocket_url=os.environ["WEBSOCKET_URL"],
            is_owner=False,
        )

    @app.route("/game/<room_id>")
    def game(room_id):
        round_duration_seconds = 30
        return render_template(
            "room.html",
            city_name="question.city_name",
            question_id="question.question_id",
            room_id=room_id,
            websocket_url=os.environ["WEBSOCKET_URL"],
            round_duration_seconds=round_duration_seconds,
        )

    @app.route("/answer", methods=["POST"])
    def answer_page():
        answer_form = request.form.get("answer")
        if not answer_form:
            abort(500)

        answer = json.loads(answer_form)
        question = closestwins_api.get_question(answer["question_id"])

        city_name = answer["city_name"]
        lat = answer["lat"]
        lng = answer["lng"]

        lat_true = question.lat
        lng_true = question.lng

        distance_object = distance.distance((lat, lng), (lat_true, lng_true))
        distance_presentation = f"{distance_object.km:.0f} km"

        if distance_object.km < 1:
            distance_presentation = f"{distance_object.m:.0f} m"
        zoom = None
        if distance_object.km < 40:
            zoom = 10
        if distance_object.km < 20:
            zoom = 11

        return render_template(
            "answer.html",
            lat_answer=lat,
            lng_answer=lng,
            lat_true=lat_true,
            lng_true=lng_true,
            distance=distance_presentation,
            city_name=city_name,
            zoom=zoom,
        )

    @app.errorhandler(500)
    def internal_server_error(_):
        return render_template("internal_server_error.html")

    return app
