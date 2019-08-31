.PHONY: poetry
poetry:
	poetry install

.PHONY: test
test: poetry lint test

.PHONY: lint
lint: 
	flake8
	poetry run black --check pytest_kind

.PHONY: test
test:
	poetry run coverage run --source=pytest_kind -m py.test
	poetry run coverage report

.PHONY: test.local
test.local:
	poetry run python3 -m http.server --directory fake-download 8000 &
	KIND_DOWNLOAD_URL=http://localhost:8000/kind poetry run coverage run --source=pytest_kind -m py.test
	poetry run coverage report
	kill %1
