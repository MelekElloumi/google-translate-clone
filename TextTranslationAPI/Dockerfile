FROM python:3.9-bullseye

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN opentelemetry-bootstrap --action=install
ENV OTEL_EXPORTER_OTLP_ENDPOINT="http://10.0.145.120:4317"
ENV OTEL_RESOURCE_ATTRIBUTES="TT_APP"


EXPOSE 8081
#CMD [ "python", "text_translation.py" ]
CMD [ "opentelemetry-instrument", "python", "./text_translation.py" ]