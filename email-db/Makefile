INTERNSHIPS_EMAIL_DB_PROJECT ?= internships-email-db-project
INTERNSHIPS_EMAIL_DB_IMAGE_VERSION ?= 0.0.1
INTERNSHIPS_EMAIL_DB_IMAGE_NAME ?= internships-email-db
INTERNSHIPS_EMAIL_DB_NAME ?= internshipsemailbackenddb
INTERNSHIPS_EMAIL_DB_USERNAME ?= internshipsemailbackenddb
INTERNSHIPS_EMAIL_DB_PASSWORD ?= internshipsemailbackenddbpwd
INTERNSHIPS_EMAIL_DB_PORT ?= 5432
INTERNSHIPS_EMAIL_DB_HOST ?= email-db
INTERNSHIPS_EMAIL_DB_DATA_PATH ?= /src/docker/internshipsv-email-db-data/
INTERNSHIPS_EMAIL_DB_PROXY_NETWORK ?= "internships-network"

.PHONY: build
build:
	docker build -t $(INTERNSHIPS_EMAIL_DB_IMAGE_NAME):$(INTERNSHIPS_EMAIL_DB_IMAGE_VERSION) -f Dockerfile .

.PHONY: run
run:
	- docker network create $(INTERNSHIPS_EMAIL_DB_PROXY_NETWORK)
	- mkdir -p $(INTERNSHIPS_EMAIL_DB_DATA_PATH)
	APP_PROXY_NETWORK=$(INTERNSHIPS_EMAIL_DB_PROXY_NETWORK) \
	APP_EMAIL_DB_IMAGE_VERSION=$(INTERNSHIPS_EMAIL_DB_IMAGE_VERSION) \
	APP_EMAIL_DB_IMAGE_NAME=$(INTERNSHIPS_EMAIL_DB_IMAGE_NAME) \
    APP_EMAIL_DB_USERNAME=$(INTERNSHIPS_EMAIL_DB_USERNAME) \
    APP_EMAIL_DB_PASSWORD=$(INTERNSHIPS_EMAIL_DB_PASSWORD) \
    APP_EMAIL_DB_NAME=$(INTERNSHIPS_EMAIL_DB_NAME) \
    APP_EMAIL_DB_PORT=$(INTERNSHIPS_EMAIL_DB_PORT) \
    APP_EMAIL_DB_HOST=$(INTERNSHIPS_EMAIL_DB_HOST) \
    APP_EMAIL_DB_DATA_PATH=$(INTERNSHIPS_EMAIL_DB_DATA_PATH) \
	docker-compose -p $(INTERNSHIPS_EMAIL_DB_PROJECT) -f docker-compose.yaml up -d
