#!/usr/bin/env python3

import connexion

from swagger_server import encoder
from swagger_server.core import init_logger


def main():
    init_logger()
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Mediator controller'}, pythonic_params=True)
    app.run(port=8089)


if __name__ == '__main__':
    main()
