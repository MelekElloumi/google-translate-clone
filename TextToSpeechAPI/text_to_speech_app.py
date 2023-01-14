from flask import Flask,jsonify
from waitress import serve
import os
import json

CONFIG_FILE="config.json"

def create_app(name):

    app = Flask(name)

    @app.route('/tts', methods=['GET'])
    def products():
        response=jsonify([0,1])
        return response


    return app



def main(production):
    app = create_app("Text_To_Speech_API")
    SECRET_KEY = os.urandom(24)
    app.secret_key = SECRET_KEY
    f = open("secrets.txt", "w")
    f.write("Tts app secret key: " + str(SECRET_KEY))
    f.close()
    if production:
        serve(app, host="127.0.0.1", port=8080)
    else:
        app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    try:
        with open(CONFIG_FILE) as config_file:
            config = json.load(config_file)
            production=config['PROD']=="True"
    except:
        print("No config file found")
    main(production)