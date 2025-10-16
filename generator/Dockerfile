FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir confluent-kafka faker

COPY tickets_generator.py /app/tickets_generator.py

CMD ["python", "tickets_generator.py"]