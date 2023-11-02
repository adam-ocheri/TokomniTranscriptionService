FROM python:3.11.4-slim

WORKDIR /

COPY .env /
COPY requirements.txt /
COPY . /

RUN apt-get update && apt-get install -y ffmpeg && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "file_server.py"]
