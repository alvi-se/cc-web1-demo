FROM python:3.12-slim

WORKDIR /app
COPY . /app/
RUN apt update && apt install iputils-ping -y
RUN pip install -r /app/requirements.txt

ENTRYPOINT [ "python", "/app/app.py" ]
