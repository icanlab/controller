#!/usr/bin/env python3

import connexion

from . import encoder
from .config import init_logger, load_app_config
from .core.datastore import datastore


def main():
    # Initialize logger before everything.
    init_logger()

    app = connexion.App(__name__, specification_dir="./swagger/")
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api(
        "swagger.yaml", arguments={"title": "Mediator controller"}, pythonic_params=True
    )

    # Load configuration.
    load_app_config(app.app)
    datastore.init_app(app.app)

    app.run(port=8089)


if __name__ == "__main__":
    main()
