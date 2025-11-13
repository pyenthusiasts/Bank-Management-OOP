"""
Main Bank class for managing multiple accounts.
"""

from typing import Dict, List, Optional, Type
from datetime import datetime

from bank_management.models import (
    BankAccount,
    CheckingAccount,
    SavingsAccount,
    BusinessAccount,
)
from bank_management.exceptions import (
    AccountNotFoundError,
    AccountAlreadyExistsError,
)
from bank_management.storage import BankStorage
from bank_management.logger import logger


class Bank:
    """
    Main bank class for managing multiple accounts.

    Attributes:
        name: Name of the bank
        accounts: Dictionary of accounts keyed by account number
        storage: Storage handler for persistence
    """

    def __init__(self, name: str = "Python Bank", storage_path: str = "bank_data.json"):
        self.name = name
        self.accounts: Dict[str, BankAccount] = {}
        self.storage = BankStorage(storage_path)
        logger.info(f"Initialized {self.name}")

    def create_account(
        self,
        account_type: str,
        account_number: str,
        account_holder: str,
        **kwargs,
    ) -> BankAccount:
        """
        Create a new bank account.

        Args:
            account_type: Type of account (checking, savings, business)
            account_number: Unique account identifier
            account_holder: Name of the account holder
            **kwargs: Additional account-specific parameters

        Returns:
            The created account instance

        Raises:
            AccountAlreadyExistsError: If account number already exists
        """
        if account_number in self.accounts:
            raise AccountAlreadyExistsError(account_number)

        # Map account types to classes
        account_classes: Dict[str, Type[BankAccount]] = {
            "checking": CheckingAccount,
            "savings": SavingsAccount,
            "business": BusinessAccount,
        }

        account_type_lower = account_type.lower()
        if account_type_lower not in account_classes:
            raise ValueError(
                f"Invalid account type: {account_type}. "
                f"Must be one of: {', '.join(account_classes.keys())}"
            )

        # Create the account
        AccountClass = account_classes[account_type_lower]
        account = AccountClass(
            account_number=account_number,
            account_holder=account_holder,
            **kwargs,
        )

        self.accounts[account_number] = account
        logger.info(f"Created {account_type} account: {account_number}")

        return account

    def get_account(self, account_number: str) -> BankAccount:
        """
        Get an account by account number.

        Args:
            account_number: Account identifier

        Returns:
            The account instance

        Raises:
            AccountNotFoundError: If account doesn't exist
        """
        if account_number not in self.accounts:
            raise AccountNotFoundError(account_number)

        return self.accounts[account_number]

    def delete_account(self, account_number: str) -> None:
        """
        Delete an account.

        Args:
            account_number: Account identifier

        Raises:
            AccountNotFoundError: If account doesn't exist
        """
        if account_number not in self.accounts:
            raise AccountNotFoundError(account_number)

        del self.accounts[account_number]
        logger.info(f"Deleted account: {account_number}")

    def list_accounts(self) -> List[BankAccount]:
        """
        Get a list of all accounts.

        Returns:
            List of all account instances
        """
        return list(self.accounts.values())

    def get_total_balance(self) -> float:
        """
        Calculate the total balance across all accounts.

        Returns:
            Total balance
        """
        return sum(account.get_balance() for account in self.accounts.values())

    def transfer(
        self,
        from_account_number: str,
        to_account_number: str,
        amount: float,
    ) -> None:
        """
        Transfer money between accounts.

        Args:
            from_account_number: Source account number
            to_account_number: Destination account number
            amount: Amount to transfer

        Raises:
            AccountNotFoundError: If either account doesn't exist
        """
        from_account = self.get_account(from_account_number)
        to_account = self.get_account(to_account_number)

        # Perform transfer
        from_account.withdraw(amount)
        to_account.deposit(amount)

        logger.info(
            f"Transferred ${amount:.2f} from {from_account_number} "
            f"to {to_account_number}"
        )

    def save(self) -> None:
        """Save all accounts to persistent storage."""
        data = {
            "bank_name": self.name,
            "accounts": {
                acc_num: acc.to_dict()
                for acc_num, acc in self.accounts.items()
            },
        }
        self.storage.save(data)
        logger.info(f"Saved {len(self.accounts)} accounts to storage")

    def load(self) -> None:
        """Load accounts from persistent storage."""
        data = self.storage.load()

        if not data:
            logger.info("No saved data found")
            return

        # Clear existing accounts
        self.accounts.clear()

        # Load bank name if available
        if "bank_name" in data:
            self.name = data["bank_name"]

        # Reconstruct accounts (simplified - would need full deserialization)
        accounts_data = data.get("accounts", {})
        logger.info(f"Loaded data for {len(accounts_data)} accounts")

        # Note: Full reconstruction would require deserializing from dict
        # This is a simplified version showing the structure

    def get_statistics(self) -> Dict[str, any]:
        """
        Get bank statistics.

        Returns:
            Dictionary containing various statistics
        """
        accounts_by_type: Dict[str, int] = {}
        total_by_type: Dict[str, float] = {}

        for account in self.accounts.values():
            acc_type = account.get_account_type()
            accounts_by_type[acc_type] = accounts_by_type.get(acc_type, 0) + 1
            total_by_type[acc_type] = (
                total_by_type.get(acc_type, 0.0) + account.get_balance()
            )

        return {
            "total_accounts": len(self.accounts),
            "total_balance": self.get_total_balance(),
            "accounts_by_type": accounts_by_type,
            "balance_by_type": total_by_type,
        }

    def __str__(self) -> str:
        """String representation of the bank."""
        return f"{self.name} - {len(self.accounts)} accounts, Total: ${self.get_total_balance():.2f}"
