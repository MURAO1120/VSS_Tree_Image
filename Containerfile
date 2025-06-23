FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates graphviz && \
    update-ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir graphviz

WORKDIR /work
ENTRYPOINT ["python"]
