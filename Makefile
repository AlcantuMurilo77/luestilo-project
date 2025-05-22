.PHONY: test

test:
	docker-compose --env-file .env.test up -d
	docker-compose exec app python -m pytest -v --cov --cov-config=.coveragerc


run:
	docker run -d --name mycontainer -p 80:80 app