# Makefile for Sample Book API
# Can be used from github workflow and locally
include .env
default: install test lint

test: lint test.all
test.cov: test.coverage

test.all:
	@pytest tests

test.coverage:
	@coverage run -m pytest -vv tests && coverage report -m --omit="*/test*,config/*.conf" --fail-under=85

install:
	@poetry install

export.schema:
	@strawberry export-schema src.graphql_api:schema > ./schema.graphql

lint:
	@pylint app tests

format.check:
	@black . --check

format.fix:
	@black .

registry.login:
	@aws ecr get-login-password --region $(AWS_REGION) | docker login --username AWS --password-stdin $(AWS_ACCOUNT).dkr.ecr.$(AWS_REGION).amazonaws.com

registry.deploy:
	@docker push $(AWS_ACCOUNT).dkr.ecr.$(AWS_REGION).amazonaws.com/book-api:latest

image.build:
	./build-image.sh

image.tag:
	@docker tag bookapi:latest $(AWS_ACCOUNT).dkr.ecr.$(AWS_REGION).amazonaws.com/book-api

image.deploy: registry.login image.tag registry.deploy

run.container:
	@docker run -d --name bookapi -p 8000:8000 bookapi

stop.container:
	@docker stop bookapi && docker rm bookapi

version.bump.patch:
	@poetry version patch

version.bump.minor:
	@poetry version minor

version.bump.major:
	@poetry version major

cdk.synth:
	@cdk synth --require-approval never

cdk.deploy:
	@cdk deploy

deployment: export.schema cdk.synth cdk.deploy

