""" This module contains the app bootstrapping code and web routes """

import toml
from debouncer import Debouncer
from flask import Flask
from flask import abort, request
from discord import Embed
from raven.contrib.flask import Sentry

app = Flask(__name__)
config = toml.load("config.toml")
debouncer = Debouncer(config)

sentry = Sentry(app=app, dsn=config['sentry'])

@app.route("/push", methods=['POST'])
def push():
    """ Handles a POST on /push with Webhook data """
    if request.headers['Authorization'] != config['token']:
        abort(401)
    if request.json is None:
        abort(400)

    embed = Embed.from_data(request.json)
    debouncer.push(embed)
    return ""

debouncer.start()
app.run(host=config['host'], port=config['port'])
