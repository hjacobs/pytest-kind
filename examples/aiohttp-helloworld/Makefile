.PHONY: docker
docker:
	docker build -t aiohttp-helloworld .

.PHONY: test
test: docker
	poetry run pytest --cluster-name=aiohttp-helloworld
