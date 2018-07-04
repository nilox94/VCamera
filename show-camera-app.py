#!/usr/bin/env python3
from bottle import Bottle, template

app = Bottle()

@app.route('/')
def index():
    return template('show-camera.html', template_lookup=['templates'])

if __name__ == '__main__':
    app.run()
