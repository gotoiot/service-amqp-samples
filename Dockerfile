FROM python:3.8

RUN mkdir /app
ADD requirements.txt /app
WORKDIR /app

ENV PYTHONPATH $PYTHONPATH:/app

RUN pip install -r requirements.txt

ADD . /app

CMD ["python", "-u", "app.py"]
