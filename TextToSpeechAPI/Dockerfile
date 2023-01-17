FROM python:3.9-bullseye

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8082
#CMD [ "python", "text_to_speech_app.py" ]
CMD ["ddtrace-run", "python", "-m", "text_to_speech_app"]