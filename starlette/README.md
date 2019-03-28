# Starlette Starter Template

## Getting Started

Build the container:

    docker-compose build

Up the container, this will also run migrations for you:

    docker-compose up

Run python migrations manually:

    docker-compose exec app sh
    alembic upgrade head

Create a new migration:

    docker-compose exec app sh
    alembic revision --autogenerate -m "first revision"
    
## Ready!!

The container is ready at http://localhost:8000/ and a mail server ready at http://localhost:8025/

## Testing

    docker-compose exec app sh
    pytest --cov=app --cov-report html
    
## Styles

npm install:

    npm install

build css:

    npm run watch-css

## View as live

To view the site as if it were running in production mode:

    docker-compose -f docker-compose-prod.yml build
    docker-compose -f docker-compose-prod.yml up

To switch back to running in dev mode you will need to build as dev dependencies will be missing.