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
	python manage.py runserver

check:
	python manage.py check

shell:
	python manage.py shell

# migrations
migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate


clean-migrations:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc" -delete

seed-data:
	python manage.py makemigrations platform_web --empty -n $(name)

newapp:
	python manage.py startapp $(name)

superuser:
	python manage.py createsuperuser

superuser-auto:
	./bash/new_superuser.sh

check-active-user:
	python manage.py dbshell 
# and then - SELECT current_user;

changepass:
	python manage.py changepassword $(user)

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

ssh-db:
	railway ssh --project=395cd9f3-6608-4f63-9c8c-bda2f1e733c7 --environment=341aa6cf-5347-4fe4-92d7-c5a77124b984 --service=cfd73612-4ce8-4a9c-af42-cba5e7924446

drop-db:
	psql -U postgres -c "DROP DATABASE IF EXISTS $(db);"
	
create-db:
	psql -U postgres -c "CREATE DATABASE $(db);"

reset-db:
	make drop-db database=$(db) && make create-db database=$(db) && rm -rf platform_web/migrations && mkdir platform_web/migrations && touch platform_web/migrations/__init__.py && make migrate && make users && make seed

users:
	./bash/setup_postgres.sh && ./bash/website_admin.sh

seed:
	cp platform_web/data/seed/*.* platform_web/migrations/

grant-public:
	psql -U postgres -d $(database) -c "GRANT ALL PRIVILEGES ON SCHEMA public TO postgres;"

reset-railway-db:
	psql -U postgres -d postgres && SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'railway'; && DROP DATABASE IF EXISTS railway; && CREATE DATABASE railway; && \c railway && GRANT ALL PRIVILEGES ON SCHEMA public TO postgres;