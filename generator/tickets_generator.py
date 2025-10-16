from confluent_kafka import Producer
from faker import Faker
import json, random, time, os
from datetime import datetime

# --- Configurer le producteur Redpanda ---
producer_conf = {
    "bootstrap.servers": "redpanda:19092"
}

producer = Producer(producer_conf)
fake = Faker()

# --- Types et priorités simulés ---
TYPES = ["support", "facturation", "technique", "commercial"]
PRIORITIES = ["basse", "normale", "haute", "critique"]

def delivery_report(err, msg):
    if err is not None:
        print(f"Échec d'envoi: {err}")
    else:
        print(f"Message produit sur {msg.topic()} partition [{msg.partition()}] offset {msg.offset()}")

# --- Boucle de production ---
ticket_id = 1
while True:
    ticket = {
        "ticket_id": ticket_id,
        "client_id": random.randint(1000, 9999),
        "created_at": datetime.now().isoformat(),
        "request": fake.sentence(),
        "type": random.choice(TYPES),
        "priority": random.choice(PRIORITIES)
    }

    producer.produce(
        topic="client_tickets",
        value=json.dumps(ticket).encode("utf-8"),
        callback=delivery_report
    )
    producer.poll(0)

    ticket_id += 1
    time.sleep(1)