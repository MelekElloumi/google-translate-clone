from flask import Flask, jsonify, request, Response, g
from flask_cors import CORS
from waitress import serve
import os
import json
from googletrans import Translator
import prometheus_client
from prometheus_client import Counter, Histogram, Gauge
from ratelimit import limits
from werkzeug.exceptions import HTTPException
import psutil
import time
import logging.config
from flask_request_id_header.middleware import RequestID

logger = logging.getLogger("Text_Translation_API")
logging.config.fileConfig('logging.ini', disable_existing_loggers=False)

CONFIG_FILE = "config.json"
prom_metrics={}
prom_metrics['translation_http_requests_total'] = Counter("translation_http_requests_total",
                                          "Number of received requests for translation api",
                                          ['endpoint','result'])
prom_metrics['translation_english_total'] = Counter("translation_english_total",
                                          "Number of english translations",
                                            ['origin'])
prom_metrics['translation_latency_seconds'] = Histogram('translation_latency_seconds', 'Latency of translation requests',['endpoint'])
prom_metrics['trasnlation_memory_usage_bytes'] = Gauge("trasnlation_memory_usage_bytes", "Memory usage in bytes.")
prom_metrics['translation_cpu_usage_percent'] = Gauge("translation_cpu_usage_percent", "CPU usage percent.")


def create_app(name):
    app = Flask(name)
    CORS(app)
    app.config['REQUEST_ID_UNIQUE_VALUE_PREFIX'] = ''
    RequestID(app)
    translator = Translator()

    @app.before_request
    def before_request():
        g.start = time.time()

    def after_request(endpoint):
        resp_time = time.time() - g.start
        prom_metrics['translation_latency_seconds'].labels(endpoint=endpoint).observe(resp_time)

    @app.errorhandler(HTTPException)
    def handle_errors(e):
        prom_metrics['translation_http_requests_total'].labels(endpoint='error', result='Fail').inc()
        logger.exception("Recieved bad http call",extra={"app": "flask","request_id":request.environ.get("HTTP_X_REQUEST_ID"),
                                                         "client_ip":request.remote_addr,"exception":e})
        return Response(
            str(e),
            status=400,
        )

    @app.route("/translate", methods=["POST"])
    @limits(calls=10, period=1)
    def translate():
        # Get the request info
        if not request.json:
            prom_metrics['translation_http_requests_total'].labels(endpoint='translate', result='Empty').inc()
            logger.warning("Empty translation request", extra={"request_id": request.environ.get("HTTP_X_REQUEST_ID"),
                                                               "client_ip": request.remote_addr,
                                                               "endpoint": "translate"})
            return jsonify({"translatedtext": ""})
        if not request.json["text"]:
            prom_metrics['translation_http_requests_total'].labels(endpoint='translate', result='Empty').inc()
            logger.warning("Empty translation request", extra={"request_id": request.environ.get("HTTP_X_REQUEST_ID"),
                                                               "client_ip": request.remote_addr,
                                                               "endpoint": "translate"})
            return jsonify({"translatedtext": ""})
        text = request.json["text"]
        source = request.json["source"]
        target = request.json["target"]
        logger.info("Translation request received", extra={"request_id": request.environ.get("HTTP_X_REQUEST_ID"),
                                               "client_ip":request.remote_addr,
                                               "endpoint":"translate","text":text,"target":target,"source":source})
        # Translate the text
        result = translator.translate(text, dest=target, src=source)
        logger.info("Translation done", extra={"request_id": request.environ.get("HTTP_X_REQUEST_ID"),
                                               "client_ip":request.remote_addr,"endpoint":"translate",
                                               "result": result.text})
        if source=="en":
            prom_metrics['translation_english_total'].labels(origin="Source").inc()
        if target=="en":
            prom_metrics['translation_english_total'].labels(origin="Target").inc()
        prom_metrics['translation_http_requests_total'].labels(endpoint='translate', result='Success').inc()
        after_request("translate")
        # Return the translation in the response
        return jsonify({"translatedtext": result.text})

    @app.route("/detect", methods=["POST"])
    @limits(calls=10, period=1)
    def detect():
        # Get the request info
        if not request.json:
            prom_metrics['translation_http_requests_total'].labels(endpoint='detect', result='Empty').inc()
            logger.warning("Empty translation request", extra={"request_id": request.environ.get("HTTP_X_REQUEST_ID"),
                                                               "client_ip": request.remote_addr,
                                                               "endpoint": "detect"})
            return jsonify({"language": ""})
        if not request.json["text"]:
            prom_metrics['translation_http_requests_total'].labels(endpoint='detect', result='Empty').inc()
            logger.warning("Empty translation request", extra={"request_id": request.environ.get("HTTP_X_REQUEST_ID"),
                                                               "client_ip": request.remote_addr,
                                                               "endpoint": "detect"})
            return jsonify({"language": ""})
        text = request.json["text"]
        print("Detecting:", text)
        logger.info("Detection request received", extra={"request_id": request.environ.get("HTTP_X_REQUEST_ID"),
                                                           "client_ip": request.remote_addr,
                                                           "endpoint": "detect", "text": text})
        # Detect the language
        result = translator.detect(text)
        logger.info("Detection done", extra={"request_id": request.environ.get("HTTP_X_REQUEST_ID"),
                                               "client_ip": request.remote_addr, "endpoint": "detection",
                                               "result": result.lang})
        print("Result detection:", result.lang)
        prom_metrics['translation_http_requests_total'].labels(endpoint='detect', result='Success').inc()
        after_request("detect")
        # Return the detection in the response
        return jsonify({"language": result.lang})

    @app.route("/metrics")
    def metrics():
        prom_metrics['trasnlation_memory_usage_bytes'].set(psutil.virtual_memory().percent)
        prom_metrics['translation_cpu_usage_percent'].set(psutil.cpu_percent())
        res=[]
        for k,v in prom_metrics.items():
            res.append(prometheus_client.generate_latest(v))
        return Response(res, mimetype="text/plain")

    return app


def main(production):
    logger.info("API started", extra={"app": "main"})
    app = create_app("Text_Translation_API")
    SECRET_KEY = os.urandom(24)
    app.secret_key = SECRET_KEY
    f = open("secrets.txt", "w")
    f.write("Text translation app secret key: " + str(SECRET_KEY))
    f.close()
    logger.info("API served", extra={"app": "main"})
    if production:
        serve(app, host="0.0.0.0", port=8081)
    else:
        app.run(port=6001)


if __name__ == '__main__':
    try:
        with open(CONFIG_FILE) as config_file:
            config = json.load(config_file)
            production = config['PROD'] == "True"
    except:
        logger.exception("No config file", extra={"app": "main"})
    main(production)
