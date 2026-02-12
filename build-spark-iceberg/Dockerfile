FROM tabulario/spark-iceberg

USER root

RUN mkdir -p /opt/spark/logs /opt/spark/work /opt/spark/conf && \
    chmod -R 777 /opt/spark/logs /opt/spark/work /opt/spark/conf /opt/spark/jars

COPY ./my_kafka_jars/*.jar /opt/spark/jars/

RUN chmod 644 /opt/spark/jars/*.jar

USER root

RUN chmod +x /opt/spark/entrypoint.sh
