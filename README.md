## Access spark-sql with catalog nessie
docker exec -it spark spark-sql \
  --conf spark.sql.catalog.nessie=org.apache.iceberg.spark.SparkCatalog \
  --conf spark.sql.catalog.nessie.uri=http://nessie:19120/api/v1 \
  --conf spark.sql.catalog.nessie.ref=main \
  --conf spark.sql.catalog.nessie.catalog-impl=org.apache.iceberg.nessie.NessieCatalog \
  --conf spark.sql.catalog.nessie.warehouse=s3a://warehouse/ \
  --conf spark.sql.catalog.nessie.io-impl=org.apache.iceberg.aws.s3.S3FileIO \
  --conf spark.hadoop.fs.s3a.endpoint=http://minio:9000 \
  --conf spark.hadoop.fs.s3a.access.key=admin \
  --conf spark.hadoop.fs.s3a.secret.key=password \
  --conf spark.hadoop.fs.s3a.path.style.access=true \
  --conf spark.sql.defaultCatalog=nessie

## Run ingest kafka to iceberg
docker exec -it spark spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1 \
  /home/iceberg/notebooks/ingest_kafka_to_iceberg.py

podman exec -it spark spark-submit /home/iceberg/notebooks/ingest_kafka_to_iceberg_vneid_hsdd_giay_to.py
  
## Port Minio
9000
9001

## Port Nessie
19120

## Port Jupyter Lab
8888

## Port Spark UI
8090

## Port Trino
8091

## Giao diện quản lý:

### Spark UI
localhost:8090

### Trino UI
localhost:8091

### Kafka UI
localhost:8080

### MinIO UI
localhost:9001

### Debezium API
localhost:8083

