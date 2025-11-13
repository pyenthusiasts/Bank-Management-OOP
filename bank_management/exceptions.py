"""
Custom exceptions for the Bank Management System.
"""


class BankingException(Exception):
    """Base exception for all banking-related errors."""
    pass


class InsufficientFundsError(BankingException):
    """Raised when an account has insufficient funds for a withdrawal."""

    def __init__(self, balance: float, amount: float):
        self.balance = balance
        self.amount = amount
        super().__init__(
            f"Insufficient funds. Balance: ${balance:.2f}, Attempted withdrawal: ${amount:.2f}"
        )


class InvalidAmountError(BankingException):
    """Raised when an invalid amount is provided for a transaction."""

    def __init__(self, amount: float, message: str = "Invalid amount provided"):
        self.amount = amount
        super().__init__(f"{message}: ${amount:.2f}")


class AccountNotFoundError(BankingException):
    """Raised when an account cannot be found."""

    def __init__(self, account_number: str):
        self.account_number = account_number
        super().__init__(f"Account not found: {account_number}")


class AccountAlreadyExistsError(BankingException):
    """Raised when attempting to create an account that already exists."""

    def __init__(self, account_number: str):
        self.account_number = account_number
        super().__init__(f"Account already exists: {account_number}")


class MinimumBalanceError(BankingException):
    """Raised when account balance falls below minimum required."""

    def __init__(self, balance: float, minimum: float):
        self.balance = balance
        self.minimum = minimum
        super().__init__(
            f"Balance ${balance:.2f} is below minimum required: ${minimum:.2f}"
        )
