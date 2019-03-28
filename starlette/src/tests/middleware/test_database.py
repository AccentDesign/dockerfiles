from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from app.auth.models import User
from app.middleware import DatabaseMiddleware


def count(request):
    users = request.state.db.query(User).count()
    return JSONResponse(
        {
            "users": users
        }
    )


app = Starlette()
app.add_middleware(DatabaseMiddleware)
app.add_route("/", count)


def test_can_use_db():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"users": 0}
