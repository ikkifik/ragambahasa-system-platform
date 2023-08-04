from apps import create_app

app = create_app('config.config')

if __name__ == "__main__":
    app.run()