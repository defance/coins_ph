PROJECT = defance_coins_ph
EXEC = docker-compose -p ${PROJECT}
BUILD_FILE = -f docker-compose.build.yaml
CONFIG_FILE := -f docker-compose.run.yaml
MANAGE_PY = python manage.py

build:
	${EXEC} ${BUILD_FILE} build app

start_db:
	@${EXEC} ${CONFIG_FILE} up -d db
	# Waiting for db to start...
	@sleep 10

configure:
	${EXEC} ${CONFIG_FILE} run --rm app ${MANAGE_PY} migrate
	${EXEC} ${CONFIG_FILE} run --rm app ${MANAGE_PY} collectstatic --noinput

test:
	${EXEC} ${CONFIG_FILE} run --rm app bash -c "pipenv install --dev --system && ${MANAGE_PY} test --settings=coins_ph.settings.autotest"

start:
	@${EXEC} ${CONFIG_FILE} up -d

stop:
	@${EXEC} ${CONFIG_FILE} down

status:
	@${EXEC} ${CONFIG_FILE} ps

logs:
	@${EXEC} ${CONFIG_FILE} logs -f --tail=0

create_superuser:
	${EXEC} ${CONFIG_FILE} run --rm app ${MANAGE_PY} createsuperuser
