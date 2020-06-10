#!/usr/bin/env python3
from bottle import Bottle, template, static_file

app = Bottle()


@app.route("/")
def index():
    return template("camera-select.html", template_lookup=["templates"])


@app.route("/static/<res:path>")
def static(res):
    return static_file(res, root="static")


if __name__ == "__main__":
    app.run()
