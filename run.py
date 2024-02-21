import config
from factory import make_app

app = make_app(config.BLOCKAID_CONFIG)

if __name__ == "__main__":
    app.run(debug=True, port=8080)
