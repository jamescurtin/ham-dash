from starlette.testclient import TestClient


def test_root_endpoint(testclient: TestClient):
    r = testclient.get("/")
    assert r.status_code == 200


def test_read_item(testclient: TestClient):
    r = testclient.get("/api/v1/example/1", params={"q": "query"})
    assert r.status_code == 200, r.text
    assert r.json()["example_id"] == 1
