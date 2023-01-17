from flask import Flask, request, send_file, Response, g
from flask_cors import CORS
from waitress import serve
import os
from gtts import gTTS
import io
import prometheus_client
from prometheus_client import Counter, Histogram, Gauge
from ratelimit import limits
from werkzeug.exceptions import HTTPException
import psutil
import time
import logging.config
from flask_request_id_header.middleware import RequestID
import traceback

logger = logging.getLogger("Text_To_Speech_API")
logging.config.fileConfig('logging.ini', disable_existing_loggers=False)

prom_metrics={}
prom_metrics['tts_http_requests_total'] = Counter("tts_http_requests_total",
                                          "Number of received requests for tts api",
                                          ['endpoint','result'])
prom_metrics['tts_english_total'] = Counter("tts_english_total",
                                          "Number of english speech",)
prom_metrics['tts_latency_seconds'] = Histogram('tts_latency_seconds', 'Latency of tts requests',['endpoint'])
prom_metrics['tts_memory_usage_bytes'] = Gauge("tts_memory_usage_bytes", "Memory usage in bytes.")
prom_metrics['tts_cpu_usage_percent'] = Gauge("tts_cpu_usage_percent", "CPU usage percent.")

def create_app(name):

    app = Flask(name)
    CORS(app)
    app.config['REQUEST_ID_UNIQUE_VALUE_PREFIX'] = ''
    RequestID(app)

    @app.before_request
    def before_request():
        g.start = time.time()

    def after_request(endpoint):
        resp_time = time.time() - g.start
        prom_metrics['tts_latency_seconds'].labels(endpoint=endpoint).observe(resp_time)

    @app.errorhandler(HTTPException)
    def handle_errors(e):
        prom_metrics['tts_http_requests_total'].labels(endpoint='error', result='Fail').inc()
        logger.exception("Recieved bad http call",
                         extra={"app": "flask", "request_id": request.environ.get("HTTP_X_REQUEST_ID"),
                                "client_ip": request.remote_addr, "exception": e})
        return Response(
            str(e),
            status=400,
        )

    @app.route('/api2/tts', methods=['GET'])
    @limits(calls=10, period=1)
    def textToSpeech():
        try:
            text=request.args.get('text')
            language=request.args.get('language')
            if not text or not language:
                prom_metrics['tts_http_requests_total'].labels(endpoint='textToSpeech', result='Empty').inc()
                logger.warning("Empty tts request", extra={"request_id": request.environ.get("HTTP_X_REQUEST_ID"),
                                                                   "client_ip": request.remote_addr,
                                                                   "endpoint": "textToSpeech"})
                return Response(status=204)
            logger.info("TextToSpeech request received", extra={"request_id": request.environ.get("HTTP_X_REQUEST_ID"),
                                                             "client_ip": request.remote_addr,
                                                             "endpoint": "textToSpeech", "text": text,"language":language})
            tts = gTTS(text=text, lang=language)
            logger.info("Speech Generation done", extra={"request_id": request.environ.get("HTTP_X_REQUEST_ID"),
                                                 "client_ip": request.remote_addr, "endpoint": "textToSpeech"})
            if language=="en":
                prom_metrics['tts_english_total'].inc()
            tts.save("tts.mp3")
            prom_metrics['tts_http_requests_total'].labels(endpoint='textToSpeech', result='Success').inc()
            after_request("textToSpeech")
            with open("tts.mp3", 'rb') as bites:
                return send_file(
                    io.BytesIO(bites.read()),
                    mimetype='audio/mp3'
                )
        except Exception:
            return Response(
                str(traceback.format_exc()),
                status=400,
            )

    @app.route("/metrics")
    def metrics():
        prom_metrics['tts_memory_usage_bytes'].set(psutil.virtual_memory().percent)
        prom_metrics['tts_cpu_usage_percent'].set(psutil.cpu_percent())
        res = []
        for k, v in prom_metrics.items():
            res.append(prometheus_client.generate_latest(v))
        return Response(res, mimetype="text/plain")

    return app



def main():
    app = create_app("Text_To_Speech_API")
    logger.info("API started", extra={"app": "main"})
    SECRET_KEY = os.urandom(24)
    app.secret_key = SECRET_KEY
    f = open("secrets.txt", "w")
    f.write("Text to Speech app secret key: " + str(SECRET_KEY))
    f.close()
    logger.info("API served", extra={"app": "main"})
    serve(app, host="0.0.0.0", port=8082)



if __name__ == '__main__':
    main()
