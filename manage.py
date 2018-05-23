from app import app
from flask import Response


@app.route("/")
def app_index():
    return Response("<h1 style='color:red'>this is the app_index</h1>")


if __name__ == "__main__":
    app.run(debug=True)
