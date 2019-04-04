# Starlette Starter Template

## Getting Started

Build the container:

```bash
docker-compose build
```

Up the container, this will also run migrations for you:

```bash
docker-compose up
```

Run python migrations manually:

```bash
docker-compose exec app sh
alembic upgrade head
```

Create a new migration:

```bash
docker-compose exec app sh
alembic revision --autogenerate -m "first revision"
```
    
## Ready!!

The container is ready at http://localhost:8000

## Testing

```bash
docker-compose exec app sh
pytest --cov=app --cov-report html
```

## Add a User

```bash
docker-compose exec app python
```

```python
>> from app.auth.models import User
>> from app.db import database
>> user = User(email='admin@example.com', first_name='Admin', last_name='User')
>> user.set_password('password')
>> database.session.add(user)
>> database.session.commit()
```

## Styles

npm install:

```bash
npm install
```

build css:

```bash
npm run watch-css
```
