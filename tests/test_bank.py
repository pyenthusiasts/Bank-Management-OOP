"""
Unit tests for Bank class.
"""

import pytest
from bank_management.bank import Bank
from bank_management.models import CheckingAccount, SavingsAccount, BusinessAccount
from bank_management.exceptions import (
    AccountNotFoundError,
    AccountAlreadyExistsError,
    InsufficientFundsError,
)


class TestBank:
    """Tests for Bank class."""

    @pytest.fixture
    def bank(self):
        """Create a bank instance for testing."""
        return Bank(name="Test Bank", storage_path="test_bank_data.json")

    def test_bank_creation(self, bank):
        """Test creating a bank."""
        assert bank.name == "Test Bank"
        assert len(bank.accounts) == 0

    def test_create_checking_account(self, bank):
        """Test creating a checking account."""
        account = bank.create_account(
            account_type="checking",
            account_number="CHK001",
            account_holder="John Doe",
            initial_balance=1000.0
        )

        assert isinstance(account, CheckingAccount)
        assert account.account_number == "CHK001"
        assert account.get_balance() == 1000.0
        assert len(bank.accounts) == 1

    def test_create_savings_account(self, bank):
        """Test creating a savings account."""
        account = bank.create_account(
            account_type="savings",
            account_number="SAV001",
            account_holder="Jane Doe",
            initial_balance=5000.0,
            interest_rate=0.03
        )

        assert isinstance(account, SavingsAccount)
        assert account.interest_rate == 0.03

    def test_create_business_account(self, bank):
        """Test creating a business account."""
        account = bank.create_account(
            account_type="business",
            account_number="BUS001",
            account_holder="John Smith",
            business_name="ABC Corp",
            tax_id="12-3456789",
            initial_balance=10000.0
        )

        assert isinstance(account, BusinessAccount)
        assert account.business_name == "ABC Corp"

    def test_duplicate_account_number(self, bank):
        """Test creating account with duplicate number."""
        bank.create_account(
            account_type="checking",
            account_number="CHK001",
            account_holder="John Doe"
        )

        with pytest.raises(AccountAlreadyExistsError):
            bank.create_account(
                account_type="savings",
                account_number="CHK001",
                account_holder="Jane Doe"
            )

    def test_invalid_account_type(self, bank):
        """Test creating account with invalid type."""
        with pytest.raises(ValueError):
            bank.create_account(
                account_type="invalid",
                account_number="INV001",
                account_holder="Test User"
            )

    def test_get_account(self, bank):
        """Test retrieving an account."""
        bank.create_account(
            account_type="checking",
            account_number="CHK001",
            account_holder="John Doe"
        )

        account = bank.get_account("CHK001")
        assert account.account_number == "CHK001"

    def test_get_nonexistent_account(self, bank):
        """Test retrieving account that doesn't exist."""
        with pytest.raises(AccountNotFoundError):
            bank.get_account("NONEXISTENT")

    def test_delete_account(self, bank):
        """Test deleting an account."""
        bank.create_account(
            account_type="checking",
            account_number="CHK001",
            account_holder="John Doe"
        )

        assert len(bank.accounts) == 1

        bank.delete_account("CHK001")
        assert len(bank.accounts) == 0

    def test_delete_nonexistent_account(self, bank):
        """Test deleting account that doesn't exist."""
        with pytest.raises(AccountNotFoundError):
            bank.delete_account("NONEXISTENT")

    def test_list_accounts(self, bank):
        """Test listing all accounts."""
        bank.create_account("checking", "CHK001", "John Doe")
        bank.create_account("savings", "SAV001", "Jane Doe")
        bank.create_account("business", "BUS001", "Company", business_name="ABC", tax_id="123")

        accounts = bank.list_accounts()
        assert len(accounts) == 3

    def test_get_total_balance(self, bank):
        """Test calculating total balance."""
        bank.create_account("checking", "CHK001", "John Doe", initial_balance=1000.0)
        bank.create_account("savings", "SAV001", "Jane Doe", initial_balance=5000.0)

        total = bank.get_total_balance()
        assert total == 6000.0

    def test_transfer(self, bank):
        """Test transferring money between accounts."""
        bank.create_account("checking", "CHK001", "John Doe", initial_balance=1000.0)
        bank.create_account("savings", "SAV001", "Jane Doe", initial_balance=5000.0, minimum_balance=0.0)

        bank.transfer("CHK001", "SAV001", 500.0)

        acc1 = bank.get_account("CHK001")
        acc2 = bank.get_account("SAV001")

        assert acc1.get_balance() == 500.0
        assert acc2.get_balance() == 5500.0

    def test_transfer_insufficient_funds(self, bank):
        """Test transfer with insufficient funds."""
        bank.create_account("checking", "CHK001", "John Doe", initial_balance=100.0, overdraft_limit=0.0)
        bank.create_account("savings", "SAV001", "Jane Doe", initial_balance=5000.0)

        with pytest.raises(InsufficientFundsError):
            bank.transfer("CHK001", "SAV001", 500.0)

    def test_transfer_nonexistent_account(self, bank):
        """Test transfer with nonexistent account."""
        bank.create_account("checking", "CHK001", "John Doe", initial_balance=1000.0)

        with pytest.raises(AccountNotFoundError):
            bank.transfer("CHK001", "NONEXISTENT", 100.0)

    def test_get_statistics(self, bank):
        """Test getting bank statistics."""
        bank.create_account("checking", "CHK001", "John Doe", initial_balance=1000.0)
        bank.create_account("savings", "SAV001", "Jane Doe", initial_balance=5000.0)
        bank.create_account("savings", "SAV002", "Bob Smith", initial_balance=3000.0)

        stats = bank.get_statistics()

        assert stats["total_accounts"] == 3
        assert stats["total_balance"] == 9000.0
        assert stats["accounts_by_type"]["CheckingAccount"] == 1
        assert stats["accounts_by_type"]["SavingsAccount"] == 2

    def test_bank_string_representation(self, bank):
        """Test string representation of bank."""
        bank.create_account("checking", "CHK001", "John Doe", initial_balance=1000.0)

        bank_str = str(bank)
        assert "Test Bank" in bank_str
        assert "1 accounts" in bank_str
