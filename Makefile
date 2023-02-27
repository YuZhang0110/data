ifeq (, $(shell which python3)||(shell which python))
	$(error "python was not found in $(PATH). For installation instructions go to https://www.python.org/downloads/.")
endif

ifeq (, $(shell which docker))
	$(error "docker was not found in $(PATH). For installation instructions go to https://docs.docker.com/get-docker/.")
endif

ifeq (, $(shell which docker-compose))
	$(error "docker-compose was not found in $(PATH). For installation instructions go to https://docs.docker.com/compose/install/.")
endif

.PHONY: dependencies
pip-install:
	pip install boto3
	pip install psycopg2
aws-configure:
	./aws_configure.sh

.PHONY: docker
start:
	docker-compose up -d
stop:
	docker-compose down --remove-orphans
clean:
	docker system prune -f

.PHONY: python3
perform-etl:
	python3 mycode.py