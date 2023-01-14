from flask import Flask, jsonify, request
from flask_cors import CORS
from waitress import serve
import os
import json
from googletrans import Translator

CONFIG_FILE = "config.json"


def create_app(name):
    app = Flask(name)
    CORS(app)
    translator = Translator()

    @app.route("/translate", methods=["POST"])
    def translate():
        # Get the request info
        if not request.json:
            return jsonify({"translatedtext": ""})
        if not request.json["text"]:
            return jsonify({"translatedtext": ""})
        text = request.json["text"]
        source = request.json["source"]
        target = request.json["target"]
        print("Input:", text, target, source)
        # Translate the text
        result = translator.translate(text, dest=target, src=source)
        print("Result:", result.text)
        # Return the translation in the response
        return jsonify({"translatedtext": result.text})

    @app.route("/detect", methods=["POST"])
    def detect():
        # Get the request info
        if not request.json:
            return jsonify({"language": ""})
        if not request.json["text"]:
            return jsonify({"language": ""})
        text = request.json["text"]
        print("Detecting:", text)
        # Translate the text
        result = translator.detect(text)

        print("Result detection:", result.lang)
        # Return the translation in the response
        return jsonify({"language": result.lang})

    return app


def main(production):
    app = create_app("Text_Translation_API")
    SECRET_KEY = os.urandom(24)
    app.secret_key = SECRET_KEY
    f = open("secrets.txt", "w")
    f.write("Text translation app secret key: " + str(SECRET_KEY))
    f.close()
    if production:
        serve(app, host="127.0.0.1", port=8081)
    else:
        app.run(port=5001)


if __name__ == '__main__':
    try:
        with open(CONFIG_FILE) as config_file:
            config = json.load(config_file)
            production = config['PROD'] == "True"
    except:
        print("No config file found")
    main(production)
