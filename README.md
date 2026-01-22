1. Start the storage:
docker run -d -p 9000:9000 -p 9001:9001 --name minio-server --network data-network -v "%cd%\minio_data:/data" -e "MINIO_ROOT_USER=admin" -e "MINIO_ROOT_PASSWORD=password" quay.io/minio/minio server /data --console-address ":9001"

2. Start the Databas:
docker run -d --name postgres-db --network data-network -p 5432:5432 -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=password -e POSTGRES_DB=warehouse postgres:15

3. Run the ETL job:
docker build -t project-etl .
docker run --rm --network data-network project-etl python etl.py

4. Verification(Optional):
docker exec -it postgres-db psql -U admin -d warehouse -c "SELECT * FROM weather_log;"