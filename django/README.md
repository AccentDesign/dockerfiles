# Django Starter Template

## Getting Started

Build the container:

    docker-compose build

Up the container, this will also run migrations for you:

    docker-compose up

Create yourself a superuser:

    docker-compose exec app bash
    python manage.py createsuperuser


Run python migrations manually:

    docker-compose exec app bash
    python manage.py migrate

## Ready!!

The container is ready at http://localhost:8000/ and a mail server ready at http://localhost:8025/

## Styles

npm install:

    npm install

build css:

    npm run watch-css
