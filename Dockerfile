FROM python:3.9-slim-bookworm
WORKDIR /app

RUN apt update -y && apt install awscli -y

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app
CMD ["python3", "app.py"]
