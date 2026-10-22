# Testing Basics with `pytest` 
The goal is to help you understand:

1. What tests are
2. Why they matter
3. How to run them
4. What each test in this project checks

---

## What are tests?
Tests are small programs that automatically check your code behavior.

Think of tests as repeatable quality checks:

- "When I call `/health`, do I get status `200`?"
- "When login is valid, do I receive a token?"
- "When login is invalid, do I get `401`?"

Instead of manually checking these each time, tests verify them for you.

## Why tests are useful

- They catch accidental erros that happen after code changes.
- They give fast feedback while you experiment and play around with new code.
- They document expected behavior.
- They build confidence before demos or submissions.


## Test tooling used in this project

This project uses [`pytest`](https://docs.pytest.org/), which is listed in `pyproject.toml`:

- `pytest>=9.1.1`

Tests live under the `tests/` folder.

## How to run tests

From the project root, run:

```cmd
uv run pytest -q
```

or use poe
```cmd
uv run poe run_tests
```

## Files in the `tests/` folder

### `tests/conftest.py`

This file adds the project root to Python’s import path so test files can import modules like:

- `from api.main import app`

Without it, you may see `ModuleNotFoundError: No module named 'api'` depending on how tests are launched.

### `tests/test_api_basics.py`

This is the main test file with beginner-friendly endpoint checks.

## What each test does

### 1) `test_health_endpoint`

Checks that:

- `GET /health` returns HTTP `200`
- body is exactly:

```json
{ "status": "ok" }
```

This is a classic "smoke test" to verify the app is up and running.


### 2) `test_games_list_returns_page_shape`

Calls:

- `GET /games?limit=5&offset=0`

Validates that the response uses the expected pagination shape:

- `items`
- `total`
- `limit`
- `offset`

Also checks `items` is a list and that its length is at most 5.

### 3) `test_auth_token_success_includes_expiry_fields`

Logs in with valid credentials:

- username: `fakeuser`
- password: `password`

Checks successful token response includes:

- `access_token`
- `token_type == "bearer"`
- `expires_in` (integer)
- `expires_at` (valid datetime)

Then confirms token expiry time is in the future.


### 4) `test_auth_token_invalid_credentials`

Attempts login with wrong password and confirms:

- HTTP `401`
- detail message: `Incorrect username or password`

This verifies failure behavior is correct and predictable.

### 5) `test_delete_requires_token`

Calls delete with no token:

- `DELETE /games/999999`

Checks for `401` unauthorized.

This proves the endpoint is protected.


### 6) `test_delete_requires_admin_role`

Logs in as normal user (`fakeuser`) and tries delete.

Expected result:

- HTTP `403`
- `Admin privileges required`

This verifies role-based authorization (`is_admin`) is enforced.

### 7) `test_delete_with_admin_token_reaches_route_logic`

Logs in as `admin`, then tries delete on a non-existent game ID.

Expected result:

- HTTP `404`
- `Game not found`

Why `404` is good here: it confirms auth succeeded and request made it into the route logic.

If admin credentials are unavailable, this test skips with a clear message.


## Reusable test pieces in this file

The test file includes:

- a `client` fixture (`TestClient(app)`) for making in-process API calls
- helper function `_login_for_token(...)` to avoid duplicate login code

These patterns keep tests short and easy to read.


## Future Proofing

When adding new endpoints, add at least 2 tests:

1. **Happy path** (works as intended)
2. **Failure path** (invalid input or permissions)

That gives you a clear picture of both successful and defensive API behavior.


## Coverage

In production environments, companies have "code coverage" guidelines, which outlines how much of the code is required to have test coverage. For most, 80% coverage is standard. 

To check this project's' code coverage, run `uv run poe coverage` in the terminal.

Right now, 81% of the code has test coverage, so we are in the clear. But as new endpoints or functions are added, this coverage will then drop and new tests would need to be added to maintian the coverage.

## Mocking

If you look at the tests, you'll notice that credentials are hard coded into the request and the production database is being queried. Obviously, this is not acceptable in a real world environment as it would both expose credentials and has the ability to have failed tests as the database changes. So what would you do instead? Mock it.

The pytest-mock library allows you to create temporary elements to simulate real functionality.

Now compare test_api.py and test_mock_api.py and review the differences. 