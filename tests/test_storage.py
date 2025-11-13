"""
Unit tests for storage functionality.
"""

import pytest
import json
from pathlib import Path
from bank_management.storage import BankStorage


class TestBankStorage:
    """Tests for BankStorage class."""

    @pytest.fixture
    def temp_storage_path(self, tmp_path):
        """Create a temporary storage path for testing."""
        return str(tmp_path / "test_bank.json")

    @pytest.fixture
    def storage(self, temp_storage_path):
        """Create a storage instance for testing."""
        return BankStorage(temp_storage_path)

    def test_storage_creation(self, storage, temp_storage_path):
        """Test creating a storage instance."""
        assert str(storage.storage_path) == temp_storage_path

    def test_save_data(self, storage):
        """Test saving data to file."""
        test_data = {
            "accounts": {
                "CHK001": {"balance": 1000.0, "holder": "John Doe"}
            }
        }

        storage.save(test_data)
        assert storage.storage_path.exists()

        # Verify file contents
        with open(storage.storage_path, "r") as f:
            saved_data = json.load(f)

        assert "data" in saved_data
        assert saved_data["data"] == test_data

    def test_load_data(self, storage):
        """Test loading data from file."""
        test_data = {
            "accounts": {
                "CHK001": {"balance": 1000.0, "holder": "John Doe"}
            }
        }

        storage.save(test_data)
        loaded_data = storage.load()

        assert loaded_data == test_data

    def test_load_nonexistent_file(self, storage):
        """Test loading from nonexistent file."""
        loaded_data = storage.load()
        assert loaded_data is None

    def test_save_creates_directory(self, tmp_path):
        """Test that save creates parent directory if needed."""
        nested_path = tmp_path / "nested" / "dir" / "bank.json"
        storage = BankStorage(str(nested_path))

        test_data = {"test": "data"}
        storage.save(test_data)

        assert nested_path.exists()

    def test_delete(self, storage):
        """Test deleting storage file."""
        test_data = {"test": "data"}
        storage.save(test_data)

        assert storage.storage_path.exists()

        storage.delete()
        assert not storage.storage_path.exists()

    def test_delete_nonexistent_file(self, storage):
        """Test deleting nonexistent file (should not raise error)."""
        storage.delete()  # Should not raise error

    def test_backup(self, storage):
        """Test creating a backup."""
        test_data = {"test": "data"}
        storage.save(test_data)

        backup_path = storage.backup()

        assert backup_path.exists()
        assert backup_path != storage.storage_path

        # Verify backup contents
        with open(backup_path, "r") as f:
            backup_data = json.load(f)

        assert backup_data["data"] == test_data

    def test_backup_custom_path(self, storage, tmp_path):
        """Test creating backup with custom path."""
        test_data = {"test": "data"}
        storage.save(test_data)

        custom_backup = tmp_path / "custom_backup.json"
        backup_path = storage.backup(str(custom_backup))

        assert backup_path == custom_backup
        assert custom_backup.exists()

    def test_backup_nonexistent_file(self, storage):
        """Test backing up nonexistent file."""
        with pytest.raises(FileNotFoundError):
            storage.backup()

    def test_metadata_in_saved_file(self, storage):
        """Test that metadata is included in saved file."""
        test_data = {"test": "data"}
        storage.save(test_data)

        with open(storage.storage_path, "r") as f:
            saved_data = json.load(f)

        assert "metadata" in saved_data
        assert "last_saved" in saved_data["metadata"]
        assert "version" in saved_data["metadata"]
