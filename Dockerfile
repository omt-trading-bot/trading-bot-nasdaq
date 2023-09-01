FROM apache/airflow:latest

USER root

# Install necessary packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

USER airflow

# Install Python packages
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Set the entrypoint
ENTRYPOINT ["/usr/bin/dumb-init", "--"]

# Start Airflow webserver and scheduler
CMD ["bash", "-c", "airflow webserver & airflow scheduler"]
