"""
Unit tests for custom exceptions.
"""

import pytest
from bank_management.exceptions import (
    BankingException,
    InsufficientFundsError,
    InvalidAmountError,
    AccountNotFoundError,
    AccountAlreadyExistsError,
    MinimumBalanceError,
)


class TestExceptions:
    """Tests for custom exceptions."""

    def test_banking_exception(self):
        """Test base BankingException."""
        with pytest.raises(BankingException) as exc_info:
            raise BankingException("Test error")

        assert str(exc_info.value) == "Test error"

    def test_insufficient_funds_error(self):
        """Test InsufficientFundsError."""
        with pytest.raises(InsufficientFundsError) as exc_info:
            raise InsufficientFundsError(balance=100.0, amount=150.0)

        exc = exc_info.value
        assert exc.balance == 100.0
        assert exc.amount == 150.0
        assert "100.00" in str(exc)
        assert "150.00" in str(exc)

    def test_invalid_amount_error(self):
        """Test InvalidAmountError."""
        with pytest.raises(InvalidAmountError) as exc_info:
            raise InvalidAmountError(amount=-50.0, message="Negative amount")

        exc = exc_info.value
        assert exc.amount == -50.0
        assert "Negative amount" in str(exc)

    def test_account_not_found_error(self):
        """Test AccountNotFoundError."""
        with pytest.raises(AccountNotFoundError) as exc_info:
            raise AccountNotFoundError(account_number="ACC123")

        exc = exc_info.value
        assert exc.account_number == "ACC123"
        assert "ACC123" in str(exc)

    def test_account_already_exists_error(self):
        """Test AccountAlreadyExistsError."""
        with pytest.raises(AccountAlreadyExistsError) as exc_info:
            raise AccountAlreadyExistsError(account_number="ACC123")

        exc = exc_info.value
        assert exc.account_number == "ACC123"
        assert "ACC123" in str(exc)

    def test_minimum_balance_error(self):
        """Test MinimumBalanceError."""
        with pytest.raises(MinimumBalanceError) as exc_info:
            raise MinimumBalanceError(balance=50.0, minimum=100.0)

        exc = exc_info.value
        assert exc.balance == 50.0
        assert exc.minimum == 100.0
        assert "50.00" in str(exc)
        assert "100.00" in str(exc)

    def test_exception_inheritance(self):
        """Test that all exceptions inherit from BankingException."""
        assert issubclass(InsufficientFundsError, BankingException)
        assert issubclass(InvalidAmountError, BankingException)
        assert issubclass(AccountNotFoundError, BankingException)
        assert issubclass(AccountAlreadyExistsError, BankingException)
        assert issubclass(MinimumBalanceError, BankingException)
