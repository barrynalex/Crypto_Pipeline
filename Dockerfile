#Dockerfile
FROM apache/airflow:2.8.1-python3.10

USER root
RUN apt-get update && apt-get install -y gcc

USER airflow
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 把 src 加到容器中
# COPY ./src /opt/airflow/src

# 設定 PYTHONPATH
ENV PYTHONPATH="/opt/airflow/src:${PYTHONPATH}"

