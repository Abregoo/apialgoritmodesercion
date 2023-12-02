FROM python:3.8-slim-buster

WORKDIR /app

ENV FLASK_APP main.py
ENV FLASK_RUN_PORT=5050

RUN apt-get update -y && \
    apt-get install -y libpq-dev python3-dev python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip install Flask gdown pandas numpy scikit-learn openpyxl flask-cors

ENV FLASK_RUN_HOST 0.0.0.0

COPY requirements.txt requirements.txt

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5050

CMD [ "flask" , "run"]