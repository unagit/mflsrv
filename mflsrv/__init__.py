import os

from flask import Flask

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY='dev',
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, 'mflsrv.sqlite'),
    )

    app.config.from_pyfile('config.py', silent=True)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # register the database commands
    from mflsrv import db
    db.init_app(app)

    # apply the blueprints to the app
    from mflsrv import auth, props
    app.register_blueprint(auth.bp)
    app.register_blueprint(props.bp)

    # make url_for('index') == url_for('props.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the props blueprint a url_prefix, but for
    # the tutorial the props will be the main index
    app.add_url_rule('/', endpoint='index')

    return app