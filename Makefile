# run:
# 	docker build -t composer-service .
# 	docker run --env-file .env -p 3000:3000 -it composer-service

composer:
	docker-compose -f deployment/docker-compose.yml up composer

connect:
	mongosh "mongodb+srv://cluster0.drjdqw7.mongodb.net/super_mongo_db" --apiVersion 1 --username super_egs_adm1n

access:
	docker exec -it mysql /bin/bash
