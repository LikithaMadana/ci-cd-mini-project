from flask import Flask

app = Flask(__name__)


def add(a, b):
    """Simple function so we have something real to unit test."""
    return a + b


@app.route("/")
def home():
    return {"message": "Hello from the CI/CD mini project"}


@app.route("/health")
def health():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
