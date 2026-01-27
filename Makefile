# poetry
add-exports:
	poetry self add poetry-plugin-export

# git
save:
	git add . && git commit
ready:
	git add . && git commit && git push

# django
run:
	poetry run python manage.py runserver

check:
	poetry run python manage.py check

shell:
	poetry run python manage.py shell

# migrations
migrate:
	poetry run python manage.py makemigrations && poetry run python manage.py migrate

showmigrations:
	poetry run python manage.py showmigrations

clean-migrations:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc" -delete

seed-data:
	python manage.py makemigrations platform_web --empty -n $(name)

newapp:
	poetry run python manage.py startapp $(name)

superuser:
	poetry run python manage.py createsuperuser

superuser-auto:
	./bash/new_superuser.sh

check-active-user:
	poetry run python manage.py dbshell 
# and then - SELECT current_user;

changepass:
	poetry run python manage.py changepassword $(user)

# deploy (railway)
requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

# postgresql
setup-postgres:
	./bash/setup_postgres.sh

drop-table:
	psql -U postgres -d code_levels -c "DROP TABLE IF EXISTS $(table) CASCADE;"

list-tables:
	psql -U postgres -d code_levels -c "\dt"

# railway
gunicorn-prod:
	gunicorn code_levels.wsgi:application

# deploy (pythonanywhere)
# 1. Create .env file on production
# 2. Check for deploy-related issues
# 3. Collect static files
# 4. Apply database migrations

secret-key-prod:
	python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

env-prod:
	chmod +x ./bash/make_env_prod.sh && ./bash/make_env_prod.sh

deploy-check:
	python manage.py check --deploy --settings=code_levels.settings.prod

check-prod:
	python manage.py check --settings=code_levels.settings.prod

static-prod:
	python manage.py collectstatic --settings=code_levels.settings.prod --noinput

migrate-prod:
	python manage.py makemigrations --settings=code_levels.settings.prod && python manage.py migrate --settings=code_levels.settings.prod

superuser-prod:
	python manage.py createsuperuser --settings=code_levels.settings.prod

run-prod:
	python manage.py runserver --settings=code_levels.settings.prod

# Helpers
activate-venv-prod:
	source ~/.venvs/myvenv/bin/activate

# frontend
frontend-install:
	npm install jquery bootstrap @fortawesome/fontawesome-free

frontend-copy:
	cp node_modules/jquery/dist/jquery.min.js static/js/libs/ && cp node_modules/bootstrap/dist/css/bootstrap.min.css static/css/libs/ && cp node_modules/bootstrap/dist/css/bootstrap.min.css.map static/css/libs/ && cp -r node_modules/@fortawesome/fontawesome-free/webfonts static/ && cp node_modules/@fortawesome/fontawesome-free/css/all.min.css static/css/libs/ && cp node_modules/bootstrap/dist/js/bootstrap.min.js static/js/libs/

fix-webfonts:
	sed -i 's|\.\./webfonts|../../webfonts|g' static/css/libs/all.min.css

frontend:
	make frontend-install && make frontend-copy && make fix-webfonts

# railway
rrun:
	railway run python manage.py runserver

up:
	railway up

# uvicorn
uvi:
	uvicorn code_levels.asgi:application \
    --host 127.0.0.1 \
    --port 8000 \

# SSH
ssh:
	railway ssh --project=395cd9f3-6608-4f63-9c8c-bda2f1e733c7 --environment=341aa6cf-5347-4fe4-92d7-c5a77124b984 --service=625bc102-6f8a-438e-9369-4dbe37e4a942

drop-db:
	psql -U postgres -c "DROP DATABASE IF EXISTS $(db);"
	
create-db:
	psql -U postgres -c "CREATE DATABASE $(database);"

reset-db:
	make drop-db database=$(database) && make create-db database=$(database) && poetry run python manage.py migrate

grant-public:
	psql -U postgres -d $(database) -c "GRANT ALL PRIVILEGES ON SCHEMA public TO postgres;"

