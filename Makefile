build:
	docker compose run frontend npm i
	docker compose up --build

up:
	docker compose up