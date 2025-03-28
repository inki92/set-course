""" Main application module """

from flask import Flask
from flask_marshmallow import Marshmallow
import connexion
import image_rec_app.config as config


def create_app(config_class=None) -> Flask:
    """ Factory method for Flask provider """
    ma = Marshmallow()
    options = {'swagger_ui': True}
    connexion_app = connexion.App(__name__,
                                  specification_dir='./openapi/',
                                  options=options)
    connexion_app.add_api('swagger.yaml')

    application = connexion_app.app
    # Load the specified configuration, if provided
    config_class = config_class or config.DevelopmentConfig

    application.config.from_object(config_class)

    ma.init_app(application)

    return application


if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=80)
