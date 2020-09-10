"""Main file used to config the app and create the endpoint.

Used on the same file since there is only one endpoint.
"""
import os

import flask

from api import config
from api import exchange

# all possible configs
configs = {
    "dev": config.DevConfig,
    "test": config.TestConfig,
    "prod": config.ProdConfig,
}

app = flask.Flask(__name__)
env = os.getenv("ENV", "test")
app.config.from_object(configs[env])

app.logger.debug(f"App initialized using env: {env}")


@app.route("/api/exchange", methods=["GET"])
def get_exchange_rate():
    """Endpoint to return the current exchange_rate."""
    sources = exchange.get_sources()
    return flask.jsonify({"rates": sources})
