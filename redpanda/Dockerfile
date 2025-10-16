# Image Redpanda stable >= 25
FROM docker.redpanda.com/redpandadata/redpanda:v25.2.8

EXPOSE 19092 19644

# Commande de démarrage du broker Redpanda
CMD ["redpanda", "start","--overprovisioned","--smp", "1","--memory", "1G","--reserve-memory", "0M","--node-id", "0","--check=false","--kafka-addr", "PLAINTEXT://0.0.0.0:19092","--advertise-kafka-addr", "PLAINTEXT://redpanda:19092","--rpc-addr", "0.0.0.0:33145","--advertise-rpc-addr", "redpanda:33145"]
