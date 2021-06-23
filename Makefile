run:
	docker-compose up

test:
	docker-compose run api python -m pytest tests; \
	docker-compose run node1 python -m pytest tests

generate:
	docker-compose run api python3 -m app.cli