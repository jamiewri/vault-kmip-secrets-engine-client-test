FROM python:3.7.9-slim
WORKDIR /usr/src/app
COPY src/requirements.txt .
RUN pip install  --no-cache-dir -r requirements.txt
COPY src/vault-kmip-test.py .
CMD ["python", "./vault-kmip-test.py"]
