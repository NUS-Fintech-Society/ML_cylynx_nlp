FROM python:3.6-slim-buster

WORKDIR /usr/src/app
COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD ["streamlit","run","app.py","--server.address","0.0.0.0"]

