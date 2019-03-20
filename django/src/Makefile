.PHONY: test

test:
	flake8
	coverage erase
	DJANGO_SETTINGS_MODULE=app.settings PYTHONPATH=. coverage run manage.py test
	coverage combine
	coverage html
	coverage report