"""
Unit tests for bank account models.
"""

import pytest
from datetime import datetime

from bank_management.models import (
    BankAccount,
    CheckingAccount,
    SavingsAccount,
    BusinessAccount,
    Transaction,
    TransactionType,
)
from bank_management.exceptions import (
    InsufficientFundsError,
    InvalidAmountError,
    MinimumBalanceError,
    BankingException,
)


class TestTransaction:
    """Tests for Transaction class."""

    def test_transaction_creation(self):
        """Test creating a transaction."""
        txn = Transaction(
            transaction_type=TransactionType.DEPOSIT,
            amount=100.0,
            balance_after=500.0,
            description="Test deposit"
        )

        assert txn.transaction_type == TransactionType.DEPOSIT
        assert txn.amount == 100.0
        assert txn.balance_after == 500.0
        assert txn.description == "Test deposit"
        assert txn.transaction_id.startswith("TXN")

    def test_transaction_to_dict(self):
        """Test converting transaction to dictionary."""
        txn = Transaction(
            transaction_type=TransactionType.WITHDRAWAL,
            amount=50.0,
            balance_after=450.0
        )

        data = txn.to_dict()
        assert data["type"] == "withdrawal"
        assert data["amount"] == 50.0
        assert data["balance_after"] == 450.0


class TestCheckingAccount:
    """Tests for CheckingAccount class."""

    def test_account_creation(self):
        """Test creating a checking account."""
        account = CheckingAccount("CHK001", "John Doe", 1000.0)

        assert account.account_number == "CHK001"
        assert account.account_holder == "John Doe"
        assert account.get_balance() == 1000.0
        assert account.get_account_type() == "CheckingAccount"

    def test_deposit(self):
        """Test depositing money."""
        account = CheckingAccount("CHK001", "John Doe", 1000.0)
        account.deposit(500.0)

        assert account.get_balance() == 1500.0

    def test_withdraw(self):
        """Test withdrawing money."""
        account = CheckingAccount("CHK001", "John Doe", 1000.0)
        account.withdraw(300.0)

        assert account.get_balance() == 700.0

    def test_invalid_deposit(self):
        """Test depositing invalid amount."""
        account = CheckingAccount("CHK001", "John Doe", 1000.0)

        with pytest.raises(InvalidAmountError):
            account.deposit(-100.0)

        with pytest.raises(InvalidAmountError):
            account.deposit(0.0)

    def test_invalid_withdrawal(self):
        """Test withdrawing invalid amount."""
        account = CheckingAccount("CHK001", "John Doe", 1000.0)

        with pytest.raises(InvalidAmountError):
            account.withdraw(-100.0)

        with pytest.raises(InvalidAmountError):
            account.withdraw(0.0)

    def test_insufficient_funds(self):
        """Test withdrawing more than balance."""
        account = CheckingAccount("CHK001", "John Doe", 100.0, overdraft_limit=50.0)

        # Should work with overdraft
        account.withdraw(120.0)
        assert account.get_balance() == -20.0

        # Should fail beyond overdraft limit
        with pytest.raises(InsufficientFundsError):
            account.withdraw(50.0)

    def test_transaction_history(self):
        """Test transaction history tracking."""
        account = CheckingAccount("CHK001", "John Doe", 1000.0)
        account.deposit(500.0)
        account.withdraw(200.0)

        history = account.get_transaction_history()
        assert len(history) >= 2  # At least deposit and withdrawal

    def test_transaction_fees(self):
        """Test transaction fees."""
        account = CheckingAccount(
            "CHK001",
            "John Doe",
            1000.0,
            transaction_fee=2.0,
            free_transactions=2
        )

        # First two transactions are free
        account.deposit(100.0)
        account.deposit(100.0)
        assert account.get_balance() == 1200.0

        # Third transaction should have fee
        account.deposit(100.0)
        assert account.get_balance() == 1298.0  # 1200 + 100 - 2


class TestSavingsAccount:
    """Tests for SavingsAccount class."""

    def test_account_creation(self):
        """Test creating a savings account."""
        account = SavingsAccount("SAV001", "Jane Doe", 5000.0, interest_rate=0.05)

        assert account.account_number == "SAV001"
        assert account.account_holder == "Jane Doe"
        assert account.get_balance() == 5000.0
        assert account.interest_rate == 0.05

    def test_deposit(self):
        """Test depositing money."""
        account = SavingsAccount("SAV001", "Jane Doe", 5000.0)
        account.deposit(1000.0)

        assert account.get_balance() == 6000.0

    def test_withdraw(self):
        """Test withdrawing money."""
        account = SavingsAccount("SAV001", "Jane Doe", 5000.0, minimum_balance=100.0)
        account.withdraw(1000.0)

        assert account.get_balance() == 4000.0

    def test_minimum_balance_violation(self):
        """Test minimum balance requirement."""
        account = SavingsAccount("SAV001", "Jane Doe", 500.0, minimum_balance=100.0)

        with pytest.raises(MinimumBalanceError):
            account.withdraw(450.0)

    def test_withdrawal_limit(self):
        """Test monthly withdrawal limit."""
        account = SavingsAccount(
            "SAV001",
            "Jane Doe",
            5000.0,
            minimum_balance=100.0,
            withdrawal_limit=3
        )

        # First 3 withdrawals should work
        account.withdraw(100.0)
        account.withdraw(100.0)
        account.withdraw(100.0)

        # 4th withdrawal should fail
        with pytest.raises(BankingException):
            account.withdraw(100.0)

    def test_add_interest(self):
        """Test adding interest."""
        account = SavingsAccount("SAV001", "Jane Doe", 1000.0, interest_rate=0.05)
        interest = account.add_interest()

        assert interest == 50.0
        assert account.get_balance() == 1050.0

    def test_reset_withdrawals(self):
        """Test resetting monthly withdrawals."""
        account = SavingsAccount("SAV001", "Jane Doe", 5000.0, withdrawal_limit=1)

        account.withdraw(100.0)

        # Reset and try again
        account.reset_monthly_withdrawals()
        account.withdraw(100.0)  # Should work

        assert account.get_balance() == 4800.0


class TestBusinessAccount:
    """Tests for BusinessAccount class."""

    def test_account_creation(self):
        """Test creating a business account."""
        account = BusinessAccount(
            "BUS001",
            "John Smith",
            "ABC Corp",
            "12-3456789",
            10000.0
        )

        assert account.account_number == "BUS001"
        assert account.account_holder == "John Smith"
        assert account.business_name == "ABC Corp"
        assert account.tax_id == "12-3456789"
        assert account.get_balance() == 10000.0

    def test_deposit(self):
        """Test depositing money."""
        account = BusinessAccount(
            "BUS001",
            "John Smith",
            "ABC Corp",
            "12-3456789",
            10000.0
        )
        account.deposit(5000.0)

        assert account.get_balance() == 15000.0

    def test_withdraw(self):
        """Test withdrawing money."""
        account = BusinessAccount(
            "BUS001",
            "John Smith",
            "ABC Corp",
            "12-3456789",
            10000.0
        )
        account.withdraw(3000.0)

        assert account.get_balance() == 7000.0

    def test_monthly_fee(self):
        """Test monthly maintenance fee."""
        account = BusinessAccount(
            "BUS001",
            "John Smith",
            "ABC Corp",
            "12-3456789",
            1000.0,
            monthly_fee=25.0
        )

        account.charge_monthly_fee()
        assert account.get_balance() == 975.0

    def test_monthly_fee_insufficient_balance(self):
        """Test monthly fee when balance is insufficient."""
        account = BusinessAccount(
            "BUS001",
            "John Smith",
            "ABC Corp",
            "12-3456789",
            10.0,
            monthly_fee=25.0
        )

        # Should not charge fee if balance is too low
        account.charge_monthly_fee()
        assert account.get_balance() == 10.0

    def test_to_dict(self):
        """Test converting to dictionary."""
        account = BusinessAccount(
            "BUS001",
            "John Smith",
            "ABC Corp",
            "12-3456789",
            10000.0
        )

        data = account.to_dict()
        assert data["account_number"] == "BUS001"
        assert data["business_name"] == "ABC Corp"
        assert data["tax_id"] == "12-3456789"
