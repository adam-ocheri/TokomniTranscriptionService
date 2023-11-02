from flask import Flask, send_file

app = Flask(__name__)


@app.route("/get_audio/<path:filename>", methods=["GET"])
def get_audio(filename):
    return send_file(filename, mimetype="audio/mpeg")


if __name__ == "__main__":
    app.run(debug=True, port=6000)
