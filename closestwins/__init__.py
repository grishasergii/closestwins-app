"""Closest wins application."""

import json
import os

from flask import Flask, render_template, request, abort, url_for, make_response
from geopy import distance

from closestwins.api.api import ClosestwinsApi
from requests.exceptions import HTTPError


def create_app():
    """Creates a flask app."""
    app = Flask(__name__)
    app.config["TRAP_HTTP_EXCEPTION"] = True
    app.jinja_env.globals.update(  # pylint: disable=no-member
        MAP_API_KEY=os.environ["MAP_API_KEY"]
    )

    closestwins_api = ClosestwinsApi(
        os.environ["REST_API_ENDPOINT"]
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

        user_name = form_data["user-name"]
        room_settings = {
            "settings": {
                "number_of_questions": int(form_data["number_of_questions"]),
                "round_duration_seconds": int(form_data["round_duration_seconds"]),
            }
        }

        room_id = closestwins_api.create_room(room_settings)
        response = make_response(render_template(
            "lobby.html",
            room_id=room_id,
            websocket_url=os.environ["WEBSOCKET_URL"],
            is_owner=True,
            invite_link=url_for("join", room_id=room_id, _external=True),
        ))
        response.set_cookie("user-name", user_name, max_age=10 * 60 * 60 * 24)
        return response

    @app.route("/join/<room_id>")
    def join(room_id):
        return render_template(
            "join_room.html",
            room_id=room_id
        )

    @app.route("/lobby/<room_id>", methods=["GET", "POST"])
    def lobby(room_id):
        response = make_response(
            render_template(
                "lobby.html",
                room_id=room_id,
                websocket_url=os.environ["WEBSOCKET_URL"],
                is_owner=False,
            )
        )

        form_data = request.form
        if form_data:
            user_name = form_data["user-name"]
            response.set_cookie("user-name", user_name, max_age=10 * 60 * 60 * 24)

        return response

    @app.route("/game/<room_id>")
    def game(room_id):
        try:
            room = closestwins_api.get_room(room_id)
        except HTTPError as error:
            if error.response.status_code == 404:
                return abort(404)
            return abort(500)

        return render_template(
            "room.html",
            city_name="question.city_name",
            question_id="question.question_id",
            room_id=room_id,
            websocket_url=os.environ["WEBSOCKET_URL"],
            round_duration_seconds=room.settings.round_duration_seconds,
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

    @app.errorhandler(404)
    def internal_server_error(_):
        return render_template("not_found_error.html")

    return app
