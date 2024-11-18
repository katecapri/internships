
.PHONY: run
run:
	- docker network create internships-network
	cd db && make build && make run && cd .. && cd migrations && make build && make run && cd .. &&  \
	cd api && make build && make run && cd ..  && cd message-broker && make build && make run && cd .. && \
	cd email-db && make build && make run && cd .. && cd api-consumer && make build && make run && cd ..  && \
	cd email-migrations && make build && make run && cd .. && \
	cd email-api && make build && make run && cd .. && cd email-consumer && make build && make run && cd .. && \
	cd points-db && make build && make run && cd .. && cd points-migrations && make build && make run && cd .. && \
	cd points-api && make build && make run && cd .. && cd points-consumer && make build && make run && cd .. && \
	cd timesheet-db && make build && make run && cd .. && cd timesheet-migrations && make build && make run && cd .. && \
	cd timesheet-api && make build && make run && cd .. && cd timesheet-consumer && make build && make run && cd ..


