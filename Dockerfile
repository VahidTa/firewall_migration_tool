FROM python:3.14-slim

WORKDIR /code

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8008

COPY . .

CMD python app.py