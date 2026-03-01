"""
test_auth.py - Unit tests for API key authentication middleware logic.
"""
import pytest
from app.models.models import AuthKey
from app.core.database import SessionLocal


def seed_key(db, api_key: str, client: str = "Test Client"):
    entry = AuthKey(api_key=api_key, client_name=client)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


class TestAuthKeyModel:
    def test_seed_and_retrieve_key(self, db):
        seed_key(db, "test-key-abc")
        result = db.query(AuthKey).filter(AuthKey.api_key == "test-key-abc").first()
        assert result is not None
        assert result.client_name == "Test Client"

    def test_invalid_key_not_found(self, db):
        seed_key(db, "valid-key-xyz")
        result = db.query(AuthKey).filter(AuthKey.api_key == "wrong-key").first()
        assert result is None

    def test_keys_are_unique(self, db):
        seed_key(db, "unique-key-123")
        from sqlalchemy.exc import IntegrityError
        with pytest.raises(IntegrityError):
            seed_key(db, "unique-key-123")

    def test_multiple_keys_for_different_clients(self, db):
        seed_key(db, "client-a-key", "Client A")
        seed_key(db, "client-b-key", "Client B")
        assert db.query(AuthKey).count() == 2
