FROM apache/spark:4.0.1-java21-python3
WORKDIR /opt/app

COPY pyspark_stream_tickets.py /opt/app/pyspark_stream_tickets.py

# JARs requis pour Kafka + dépendances
RUN curl -L -o /opt/spark/jars/spark-sql-kafka-0-10_2.13-4.0.1.jar \
      https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.13/4.0.1/spark-sql-kafka-0-10_2.13-4.0.1.jar && \
    curl -L -o /opt/spark/jars/spark-token-provider-kafka-0-10_2.13-4.0.1.jar \
      https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.13/4.0.1/spark-token-provider-kafka-0-10_2.13-4.0.1.jar && \
    curl -L -o /opt/spark/jars/kafka-clients-3.8.0.jar \
      https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.8.0/kafka-clients-3.8.0.jar && \
    curl -L -o /opt/spark/jars/commons-pool2-2.12.0.jar \
      https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.12.0/commons-pool2-2.12.0.jar

CMD ["/opt/spark/bin/spark-submit","/opt/app/pyspark_stream_tickets.py"]