from fastapi.testclient import TestClient
import sys
import os
from app.main import app 

client = TestClient(app) 

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200

def test_login():
    response = client.get("/login")
    assert response.status_code == 200

def test_read_token():
    response = client.post("/v1/token", data={"username": "antonio@antonio.mas", "password": "1234"})
    assert response.status_code == 200

def test_read_and_not_login_ist_ok():
    response = client.post("/v1/token", data={"username": "error@error.er", "password": "4321"})
    assert response.status_code == 400