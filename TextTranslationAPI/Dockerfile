FROM python:3.9-bullseye

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8081
#CMD [ "python", "text_translation.py" ]
CMD ["ddtrace-run", "python", "-m", "text_translation"]