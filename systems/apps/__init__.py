from flask import Flask, jsonify, render_template
from flask_cors import CORS
from apps.models import db, Users

app = Flask(__name__)
CORS(app)
def create_app(config_file):

    app.config.from_object(config_file)
    db.init_app(app)
    app.secret_key = "48_ze3"
    
    # registering blueprint
    # from apps.home import bp as home_bp
    # app.register_blueprint(home_bp, url_prefix='/')
    
    from apps.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/access/')
    
    from apps.apis import bp as apis_bp
    app.register_blueprint(apis_bp, url_prefix='/api/')
    
    @app.errorhandler(404)
    def page_not_found(e):
        # note that we set the 404 status explicitly
        print(e)
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_server(e):
        # note that we set the 500 status explicitly
        print(e)
        return render_template('500.html'), 500

    return app