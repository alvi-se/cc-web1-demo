FROM python:3.12-slim

RUN apt update && apt install iputils-ping curl -y
WORKDIR /app
COPY . /app/
RUN pip install -r /app/requirements.txt
RUN touch 'red-button'

ENTRYPOINT [ "python", "/app/app.py" ]
