from apps import create_app

app = create_app('config.config')

if __name__ == "__main__":
    app.run(host=app.config['FLASK_HOST'], 
            port=app.config['FLASK_PORT'], 
            debug=app.config['DEBUG'])