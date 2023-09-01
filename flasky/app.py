from flask import Flask, render_template, request

import redis
from redis.commands.search.query import Query
import mysql.connector
from datamanager import DataManager


app = Flask(__name__)
dm = DataManager()

@app.route("/", methods=["GET", "POST"])
def show_form():
    return render_template("index.html")


@app.route("/result", methods=["POST"])
def show_result():
    if request.method == "POST":
        data = request.form.to_dict()
        result = getResultsFromBackend(data)
        # mocking the result =
        # result = data = [
        #     (
        #         5198,
        #         "Maruti Vitara Brezza ZXI Plus AT Dual Tone",
        #         2020,
        #         737000,
        #         10000,
        #         "Petrol",
        #         "Individual",
        #         "Automatic",
        #         5.33,
        #         1462,
        #         103,
        #         5,
        #     ),
        #     (
        #         2156,
        #         "Hyundai i20 1.4 Magna AT",
        #         2018,
        #         700000,
        #         42000,
        #         "Petrol",
        #         "Individual",
        #         "Automatic",
        #         5.38,
        #         1368,
        #         99,
        #         5,
        #     ),
        #     (
        #         1434,
        #         "Tata Tiago 1.2 Revotron XZA",
        #         2019,
        #         550000,
        #         30000,
        #         "Petrol",
        #         "Individual",
        #         "Automatic",
        #         4.19,
        #         1199,
        #         84,
        #         5,
        #     ),
        #     (
        #         4313,
        #         "Hyundai i20 1.4 Magna AT",
        #         2018,
        #         671000,
        #         20000,
        #         "Petrol",
        #         "Individual",
        #         "Automatic",
        #         5.38,
        #         1368,
        #         99,
        #         5,
        #     ),
        #     (
        #         5395,
        #         "Maruti Swift Dzire AMT VXI BS IV",
        #         2019,
        #         700000,
        #         45000,
        #         "Petrol",
        #         "Individual",
        #         "Automatic",
        #         4.55,
        #         1197,
        #         82,
        #         5,
        #     ),
        # ]
    return render_template("results.html", vehicules=result)


def getResultsFromBackend(data):
    print(data)
    keys_to_convert = ["year", "selling_price", "km_driven", "mileage", "engine", "max_power", "seats"]
    for key in keys_to_convert:
            data[key] = int(float(data[key]))
    res = dm.query(data)
    print(res)
    return res


if __name__ == "__main__":
    app.run(debug=True)
