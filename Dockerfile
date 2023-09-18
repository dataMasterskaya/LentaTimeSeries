FROM python:3.10-slim

COPY requirements.txt /app/requirements.txt
COPY backend /app
COPY ml /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "app.py"]