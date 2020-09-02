# Pull base image
FROM python:3.7

RUN mkdir -p /app/eu4

WORKDIR /app/eu4

COPY . .

RUN pip install -r ./requirements.txt

EXPOSE 5000

CMD ["python", "run.py"]