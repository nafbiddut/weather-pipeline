1. Download the files. 
2. Install docker if not installed. 
3. run this command: docker-compose up --build
4. Verification(Optional): docker exec -it postgres-db psql -U admin -d warehouse -c "SELECT * FROM weather_log;"
5. To view the dashboard, go this link: http://localhost:3000 (Host: postgres-db, User: admin, Pass: password)
