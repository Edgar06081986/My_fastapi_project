.PHONY: backup restore down clean up build

backup:
	docker exec -t postgainer pg_dump -U postgres -d postgres > backup.sql

restore:
	docker exec -i postgainer psql -U postgres -d postgres < backup.sql

down:
	docker compose down

clean:
	docker compose down -v

up:
	docker compose up -d

build:
	docker compose up --build -d
