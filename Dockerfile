FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 4000

CMD python ./run.py 