import os
import json
import random
from geopy import distance
from flask import Flask, render_template, request


app = Flask(__name__)
app.jinja_env.globals.update(MAP_API_KEY=os.environ["MAP_API_KEY"])

cities = {
        "London": (51.509865, -0.118092),
        "New York": (40.730610, -73.935242),
        "Houston": (29.749907, -95.358421),
        "Cairo": (30.033333, 31.233334),
        "New Delhi": (28.644800, 77.216721),
        "Caracas": (10.500000, -66.916664),
        "Santiago": (-33.447487, -70.673676)
    }


@app.route("/")
def question_page():
    city_name = random.choice(list(cities.keys()))
    return render_template("question.html", city=city_name)


@app.route("/answer", methods=["POST"])
def answer_page():
    answer = json.loads(request.form.get("answer", "not found"))
    print(answer)
    lat = answer["lat"]
    lng = answer["lng"]
    city = answer["city"]
    lat_true, lng_true = cities[city]
    distance_object = distance.distance((lat, lng), (lat_true, lng_true))
    distance_presentation = f"{distance_object.km:.0f} km"
    if distance_object.km < 1:
        distance_presentation = f"{distance_object.m:.0f} m"
    return render_template("answer.html", lat_answer=lat, lng_answer=lng, lat_true=lat_true, lng_true=lng_true, distance=distance_presentation, city=city)


if __name__ == "__main__":
    app.run(debug=True)
