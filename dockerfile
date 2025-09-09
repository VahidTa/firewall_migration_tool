FROM python:3.10-slim

WORKDIR /code

COPY requirements.txt requirements.txt

RUN apt-get -y update
RUN pip install -r requirements.txt

EXPOSE 5000

COPY . .

CMD python app.py