from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, IntegerType, TimestampType

# ---  Session Spark ---
spark = (
    SparkSession.builder
    .appName("RedpandaClientTicketsStreaming")
    .config("spark.sql.streaming.stopGracefullyOnShutdown", "true")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

# --- Schéma des messages ---
schema = (
    StructType()
    .add("ticket_id", IntegerType())
    .add("client_id", IntegerType())
    .add("created_at", StringType())
    .add("request", StringType())
    .add("type", StringType())
    .add("priority", StringType())
)

# --- flux depuis Redpanda ---
df_raw = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "redpanda:19092")
    .option("subscribe", "client_tickets")
    .option("startingOffsets", "earliest")
    .option("failOnDataLoss", "false")         
    .option("kafka.retry.backoff.ms", "1000")
    .option("kafka.reconnect.backoff.max.ms", "10000")
    .load()
)

# --- Parse les messages JSON ---
df_parsed = (
    df_raw
    .selectExpr("CAST(value AS STRING) as json")
    .select(from_json(col("json"), schema).alias("data"))
    .select("data.*")
)

# --- Traitement simple ---
df_agg = (
    df_parsed
    .groupBy("type", "priority")
    .count()
)

# --- Export JSON en parallèle ---
def export_json(batch_df, epoch_id):
    out = f"/tmp/agg_json/epoch={epoch_id}"
    (batch_df.coalesce(1)
            .write.mode("overwrite")
            .json(out))

# --- Sortie console ---
query = (
    df_agg
    .writeStream
    .outputMode("complete")
    .format("console")
    .option("truncate", False)
    .option("checkpointLocation", "/opt/spark/checkpoints/agg")
    .start()
)

# --- Export JSON ---
json_query = (
    df_agg
    .writeStream
    .outputMode("complete")
    .foreachBatch(export_json)
    .option("checkpointLocation", "/opt/spark/checkpoints/agg_json")
    .trigger(processingTime="10 seconds")
    .start()
)

spark.streams.awaitAnyTermination()