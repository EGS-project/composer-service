run:
	docker build -t composer-service .
	docker run --env-file .env -p 3000:3000 -it composer-service
