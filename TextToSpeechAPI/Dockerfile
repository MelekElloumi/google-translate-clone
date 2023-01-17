FROM python:3.9-bullseye

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN opentelemetry-bootstrap --action=install
ENV OTEL_EXPORTER_OTLP_ENDPOINT="http://10.0.145.120:4317"
ENV OTEL_RESOURCE_ATTRIBUTES="TTS_APP"
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION="python"

EXPOSE 8082
#CMD [ "python", "text_to_speech_app.py" ]
CMD [ "opentelemetry-instrument", "python", "./text_to_speech_app.py" ]