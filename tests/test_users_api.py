import time
import requests

BASE = "https://jsonplaceholder.typicode.com"

session = requests.Session()
session.trust_env = False


def test_get_post_ok():
    t0 = time.time()
    r = session.get(f"{BASE}/posts/1", timeout=20)
    elapsed_ms = (time.time() - t0) * 1000

    assert r.status_code == 200
    assert "application/json" in (r.headers.get("Content-Type") or "")
    assert elapsed_ms <= 1500

    body = r.json()
    assert set(body.keys()) == {"userId", "id", "title", "body"}
    assert body["id"] == 1
    assert isinstance(body["title"], str) and body["title"].strip() != ""


def test_create_post_ok():
    payload = {"title": "Hello", "body": "World", "userId": 10}
    r = session.post(f"{BASE}/posts", json=payload, timeout=20)

    assert r.status_code == 201
    assert "application/json" in (r.headers.get("Content-Type") or "")

    body = r.json()
    assert body["title"] == "Hello"
    assert body["body"] == "World"
    assert body["userId"] == 10
    assert "id" in body


def test_update_post_ok():
    payload = {"id": 1, "title": "Updated", "body": "Text", "userId": 1}
    r = session.put(f"{BASE}/posts/1", json=payload, timeout=20)

    assert r.status_code == 200
    assert "application/json" in (r.headers.get("Content-Type") or "")
    body = r.json()
    assert body["title"] == "Updated"
    assert body["id"] == 1
    assert body["userId"] == 1


def test_not_found():
    r = session.get(f"{BASE}/__unknown__", timeout=20)
    assert r.status_code == 404
