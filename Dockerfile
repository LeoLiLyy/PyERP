FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt requirements.txt
COPY requirements.txt aaa.txt

RUN apt-get update && apt-get install -y gcc && apt-get install -y build-essential && apt-get install -y font-manager
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y default-mysql-client

COPY . .

# CMD ["uwsgi", "--socket", "0.0.0.0:5000", "--protocol", "http", "-w", "wsgi:app"]
CMD ["uwsgi", "--ini", "uwsgi.ini"]