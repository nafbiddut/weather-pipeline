FROM python:3.9-slim
WORKDIR /app
RUN pip install boto3 requests psycopg2-binary
COPY *.py .
CMD ["python", "main.py"]