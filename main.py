from pyspark.sql import SparkSession

# Create Spark session
spark = SparkSession.builder \
    .appName("HelloSpark") \
    .getOrCreate()

# Print something — via Spark, not just Python
df = spark.createDataFrame([(1, "Hello from Spark"), (2, "🔥 it works!")], ["id", "message"])
df.show()

spark.stop()
