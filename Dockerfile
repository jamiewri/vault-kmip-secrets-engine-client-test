FROM python:3.7.9-slim
WORKDIR /usr/src/app
COPY src/ .
RUN pip install  --no-cache-dir -r requirements.txt
CMD ["python", "vault-kmip-test.py"]
