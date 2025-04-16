# conftest.py
import pytest

@pytest.fixture(autouse=True)
def patch_getpass(monkeypatch):
    # Automatically monkeypatch getpass in every test
    monkeypatch.setattr('getpass.getpass', lambda prompt: "csrocks")

@pytest.fixture(autouse=True)
def patch_sleep(monkeypatch):
    # Automatically monkeypatch getpass in every test
    monkeypatch.setattr('time.sleep', lambda input: None)
