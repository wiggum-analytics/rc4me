IMAGE=rc4me
PROJ_DIR="rc4me"

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build-docker:
	docker build -t $(IMAGE):latest .

bash: build-docker
	docker run -it $(IMAGE):latest bash

dev: build-docker
	docker run -v ${PWD}:/mnt -w /mnt -it $(IMAGE):latest bash

ci-black: build-docker ## Test lint compliance using black. Config in pyproject.toml file
	docker run --rm $(IMAGE) black --check $(PROJ_DIR)

ci-flake8: build-docker ## Test lint compliance using flake8. Config in tox.ini file
	docker run --rm $(IMAGE) flake8 $(PROJ_DIR)

ci-test: build-docker ## Runs unit tests using pytest
	docker run --rm $(IMAGE) pytest $(PROJ_DIR)

ci: ci-black ci-flake8 ci-test ## Check black, flake8, and run unit tests
	@echo "CI sucessful"

isort: build-docker  ## Runs isort to sorts imports
	docker run -v ${PWD}:/mnt -w /mnt -it $(IMAGE) isort $(PROJ_DIR)

black: build-docker ## Runs black auto-formater
	docker run -v ${PWD}:/mnt -w /mnt -it $(IMAGE) black $(PROJ_DIR)

format: isort black ## Lints repo; runs black and isort on all files
	@echo "Linting complete"

install:
	pip install .
