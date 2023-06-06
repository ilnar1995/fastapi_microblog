pipenv run alembic revision --autogenerate -m 'fixed column date in user model'
pipenv run alembic upgrade head