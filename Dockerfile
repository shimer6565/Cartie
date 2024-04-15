FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt 

RUN pip install -r requirements.txt

COPY . .

EXPOSE 4000

CMD ["python3", "run.py"]