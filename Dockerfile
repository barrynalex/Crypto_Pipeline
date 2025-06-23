# Dockerfile
FROM apache/airflow:2.8.1-python3.10

USER root
# 安裝任何 OS 依賴（可選）
RUN apt-get update && apt-get install -y gcc

USER airflow
# 安裝你需要的 Python 套件
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt
