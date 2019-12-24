.PHONY: install
install:
	poetry install

.PHONY: lint
lint: install
	poetry run flake8
	poetry run black --check pytest_kind
	poetry run mypy --ignore-missing-imports pytest_kind

.PHONY: test
test: lint
	poetry run coverage run --source=pytest_kind -m py.test tests/
	poetry run coverage report

.PHONY: test.local
test.local: poetry lint
	poetry run python3 -m http.server --directory fake-download 8000 &
	KIND_DOWNLOAD_URL=http://localhost:8000/kind poetry run coverage run --source=pytest_kind -m py.test -v tests/
	poetry run coverage report

.PHONY: mirror
mirror:
	git push --mirror git@github.com:hjacobs/pytest-kind.git
