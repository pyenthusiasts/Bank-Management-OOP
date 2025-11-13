"""
Data persistence layer for the Bank Management System.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

from bank_management.logger import logger


class BankStorage:
    """
    Handles saving and loading bank data to/from JSON files.

    Attributes:
        storage_path: Path to the storage file
    """

    def __init__(self, storage_path: str = "bank_data.json"):
        self.storage_path = Path(storage_path)
        logger.info(f"Initialized BankStorage with path: {self.storage_path}")

    def save(self, data: Dict[str, Any]) -> None:
        """
        Save bank data to JSON file.

        Args:
            data: Dictionary containing bank data to save
        """
        try:
            # Add metadata
            save_data = {
                "metadata": {
                    "last_saved": datetime.now().isoformat(),
                    "version": "2.0.0",
                },
                "data": data,
            }

            # Ensure parent directory exists
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)

            # Write to file with pretty formatting
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)

            logger.info(f"Successfully saved data to {self.storage_path}")

        except Exception as e:
            logger.error(f"Error saving data: {e}")
            raise

    def load(self) -> Optional[Dict[str, Any]]:
        """
        Load bank data from JSON file.

        Returns:
            Dictionary containing bank data, or None if file doesn't exist
        """
        if not self.storage_path.exists():
            logger.warning(f"Storage file not found: {self.storage_path}")
            return None

        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                save_data = json.load(f)

            # Extract data from wrapper
            data = save_data.get("data", save_data)

            # Log metadata if available
            if "metadata" in save_data:
                metadata = save_data["metadata"]
                logger.info(
                    f"Loaded data from {self.storage_path} "
                    f"(saved: {metadata.get('last_saved', 'unknown')})"
                )
            else:
                logger.info(f"Loaded data from {self.storage_path}")

            return data

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in storage file: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise

    def delete(self) -> None:
        """Delete the storage file."""
        if self.storage_path.exists():
            self.storage_path.unlink()
            logger.info(f"Deleted storage file: {self.storage_path}")
        else:
            logger.warning(f"Storage file not found: {self.storage_path}")

    def backup(self, backup_path: Optional[str] = None) -> Path:
        """
        Create a backup of the storage file.

        Args:
            backup_path: Optional custom backup path

        Returns:
            Path to the backup file
        """
        if not self.storage_path.exists():
            raise FileNotFoundError(f"No storage file to backup: {self.storage_path}")

        if backup_path:
            backup = Path(backup_path)
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup = self.storage_path.parent / f"{self.storage_path.stem}_backup_{timestamp}.json"

        # Ensure backup directory exists
        backup.parent.mkdir(parents=True, exist_ok=True)

        # Copy file
        import shutil
        shutil.copy2(self.storage_path, backup)

        logger.info(f"Created backup: {backup}")
        return backup
