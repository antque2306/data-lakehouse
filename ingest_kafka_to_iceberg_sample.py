from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, coalesce
from pyspark.sql.types import StructType, StringType, IntegerType

# 1. Khởi tạo Spark Session (đã cấu hình sẵn trong container tabulario)
spark = SparkSession.builder \
    .appName("KafkaToIceberg") \
    .getOrCreate()

# 2. Định nghĩa Schema cho dữ liệu Debezium (tùy biến theo bảng của bạn)
# Ở đây tôi giả lập schema cho bảng 'users' đơn giản
schema = StructType() \
    .add("id", IntegerType()) \
    .add("first_name", StringType()) \
    .add("last_name", StringType()) \
    .add("email", StringType())

# 3. Định nghĩa schema tổng cho message Kafka
# Cấu trúc: { "after": {...}, "op": "..." }
root_schema = StructType() \
    .add("before", schema) \
    .add("after", schema) \
    .add("op", StringType())

# 4. Đọc dữ liệu từ Kafka
# Chúng ta subscribe vào topic mà Debezium đã tạo
raw_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "mysql_db.inventory_db_mysql.customers") \
    .option("startingOffsets", "earliest") \
    .load()

# 5. Xử lý dữ liệu CDC từ Debezium
# Debezium bọc dữ liệu trong payload.after. Chúng ta cần trích xuất nó ra.
# Lưu ý: Vì bạn tắt Schemas enable nên value là JSON thuần.
json_df = raw_df.selectExpr("CAST(value AS STRING) as json_str") \
    .select(from_json(col("json_str"), root_schema).alias("data")) \
    .select(
        coalesce(col("data.after.id"), col("data.before.id")).alias("id"),
        col("data.after.first_name").alias("first_name"),
        col("data.after.last_name").alias("last_name"),
        col("data.after.email").alias("email"),
        col("data.op").alias("op")
    )

# 6. Ghi dữ liệu vào Iceberg Table qua Catalog Nessie
# 'append' sẽ thêm dữ liệu mới vào bảng liên tục
query = json_df.writeStream \
    .format("iceberg") \
    .outputMode("append") \
    .option("path", "nessie.bronze.users_cdc") \
    .option("checkpointLocation", "/tmp/checkpoints/users_ingestion_v2") \
    .start()

print("🚀 Pipeline đang chạy... Đang bơm dữ liệu từ Kafka vào Iceberg!")
query.awaitTermination()
