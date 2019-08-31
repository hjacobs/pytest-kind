.PHONY: docker
docker:
	docker build -t hjacobs/aiohttp-helloworld:latest .

.PHONY: test
test: docker
	poetry install
	poetry run pytest --cluster-name=aiohttp-helloworld
