from fastapi.testclient import TestClient
from app import auth
from app.main import app


def authenticated_client(test):
    # Feature tests focus on payloads; authentication has dedicated integration tests.
    app.dependency_overrides[auth.require_user] = lambda: {'id': 1, 'username': 'fixture'}
    test.addCleanup(lambda: app.dependency_overrides.pop(auth.require_user, None))
    return TestClient(app, headers={'X-Finite-Request': '1'})
