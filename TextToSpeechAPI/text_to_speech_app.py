from flask import Flask, request, send_file, Response
from flask_cors import CORS
from waitress import serve
import os
import json
from gtts import gTTS
import io
CONFIG_FILE="config.json"

def create_app(name):

    app = Flask(name)
    CORS(app)

    @app.route('/tts', methods=['GET'])
    def textToSpeech():
        text=request.args.get('text')
        language=request.args.get('language')
        if not text or not language:
            return Response(status=204)
        print(text,language)
        tts = gTTS(text=text, lang=language)
        tts.save("temp_audio/tts.mp3")

        with open("temp_audio/tts.mp3", 'rb') as bites:
            return send_file(
                io.BytesIO(bites.read()),
                attachment_filename='tts.mp3',
                mimetype='audio/mp3'
            )

    return app



def main(production):
    app = create_app("Text_To_Speech_API")
    SECRET_KEY = os.urandom(24)
    app.secret_key = SECRET_KEY
    f = open("secrets.txt", "w")
    f.write("Text to Speech app secret key: " + str(SECRET_KEY))
    f.close()
    if production:
        serve(app, host="127.0.0.1", port=8080)
    else:
        app.run(port=5000)


if __name__ == '__main__':
    try:
        with open(CONFIG_FILE) as config_file:
            config = json.load(config_file)
            production=config['PROD']=="True"
    except:
        print("No config file found")
    main(production)
