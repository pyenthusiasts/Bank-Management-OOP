"""
Bank account models implementing various account types.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum

from bank_management.exceptions import (
    InsufficientFundsError,
    InvalidAmountError,
    MinimumBalanceError,
)


class TransactionType(Enum):
    """Enumeration of transaction types."""
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    INTEREST = "interest"
    FEE = "fee"


class Transaction:
    """
    Represents a single transaction on a bank account.

    Attributes:
        transaction_id: Unique identifier for the transaction
        transaction_type: Type of transaction (deposit, withdrawal, etc.)
        amount: Transaction amount
        timestamp: When the transaction occurred
        balance_after: Account balance after transaction
        description: Optional description of the transaction
    """

    def __init__(
        self,
        transaction_type: TransactionType,
        amount: float,
        balance_after: float,
        description: str = "",
    ):
        self.transaction_id = self._generate_transaction_id()
        self.transaction_type = transaction_type
        self.amount = amount
        self.timestamp = datetime.now()
        self.balance_after = balance_after
        self.description = description

    @staticmethod
    def _generate_transaction_id() -> str:
        """Generate a unique transaction ID."""
        return f"TXN{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

    def to_dict(self) -> Dict[str, Any]:
        """Convert transaction to dictionary."""
        return {
            "transaction_id": self.transaction_id,
            "type": self.transaction_type.value,
            "amount": self.amount,
            "timestamp": self.timestamp.isoformat(),
            "balance_after": self.balance_after,
            "description": self.description,
        }

    def __str__(self) -> str:
        """String representation of the transaction."""
        return (
            f"{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} | "
            f"{self.transaction_type.value.upper():12} | "
            f"${self.amount:>10.2f} | "
            f"Balance: ${self.balance_after:>10.2f}"
        )


class BankAccount(ABC):
    """
    Abstract base class representing a generic bank account.

    Attributes:
        account_number: Unique account identifier
        account_holder: Name of the account holder
        balance: Current account balance
        created_at: Account creation timestamp
        transactions: History of all transactions
    """

    def __init__(
        self,
        account_number: str,
        account_holder: str,
        initial_balance: float = 0.0,
    ):
        if initial_balance < 0:
            raise InvalidAmountError(initial_balance, "Initial balance cannot be negative")

        self.account_number = account_number
        self.account_holder = account_holder
        self._balance = initial_balance
        self.created_at = datetime.now()
        self._transactions: List[Transaction] = []

        if initial_balance > 0:
            self._record_transaction(
                TransactionType.DEPOSIT,
                initial_balance,
                "Initial deposit"
            )

    @abstractmethod
    def deposit(self, amount: float) -> None:
        """Deposit money into the account."""
        pass

    @abstractmethod
    def withdraw(self, amount: float) -> None:
        """Withdraw money from the account."""
        pass

    def get_balance(self) -> float:
        """Get the current account balance."""
        return self._balance

    def _record_transaction(
        self,
        transaction_type: TransactionType,
        amount: float,
        description: str = "",
    ) -> None:
        """Record a transaction in the transaction history."""
        transaction = Transaction(
            transaction_type=transaction_type,
            amount=amount,
            balance_after=self._balance,
            description=description,
        )
        self._transactions.append(transaction)

    def get_transaction_history(self, limit: Optional[int] = None) -> List[Transaction]:
        """
        Get transaction history for the account.

        Args:
            limit: Optional limit on number of transactions to return

        Returns:
            List of transactions (most recent first)
        """
        transactions = sorted(
            self._transactions,
            key=lambda t: t.timestamp,
            reverse=True
        )
        return transactions[:limit] if limit else transactions

    def get_account_type(self) -> str:
        """Get the type of account."""
        return self.__class__.__name__

    def to_dict(self) -> Dict[str, Any]:
        """Convert account to dictionary for serialization."""
        return {
            "account_number": self.account_number,
            "account_holder": self.account_holder,
            "account_type": self.get_account_type(),
            "balance": self._balance,
            "created_at": self.created_at.isoformat(),
            "transactions": [t.to_dict() for t in self._transactions],
        }

    def __str__(self) -> str:
        """String representation of the account."""
        return (
            f"{self.get_account_type()}: {self.account_number} | "
            f"Holder: {self.account_holder} | "
            f"Balance: ${self._balance:.2f}"
        )

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return (
            f"{self.__class__.__name__}("
            f"account_number='{self.account_number}', "
            f"account_holder='{self.account_holder}', "
            f"balance={self._balance})"
        )


class CheckingAccount(BankAccount):
    """
    Checking account with overdraft protection and transaction fees.

    Attributes:
        overdraft_limit: Maximum negative balance allowed
        transaction_fee: Fee charged per transaction
        free_transactions: Number of free transactions per month
    """

    def __init__(
        self,
        account_number: str,
        account_holder: str,
        initial_balance: float = 0.0,
        overdraft_limit: float = 100.0,
        transaction_fee: float = 0.0,
        free_transactions: int = 5,
    ):
        super().__init__(account_number, account_holder, initial_balance)
        self.overdraft_limit = overdraft_limit
        self.transaction_fee = transaction_fee
        self.free_transactions = free_transactions
        self._monthly_transactions = 0

    def deposit(self, amount: float) -> None:
        """Deposit money into the checking account."""
        if amount <= 0:
            raise InvalidAmountError(amount, "Deposit amount must be positive")

        self._balance += amount
        self._record_transaction(TransactionType.DEPOSIT, amount, "Deposit")
        self._apply_transaction_fee()

    def withdraw(self, amount: float) -> None:
        """Withdraw money from the checking account."""
        if amount <= 0:
            raise InvalidAmountError(amount, "Withdrawal amount must be positive")

        if amount > self._balance + self.overdraft_limit:
            raise InsufficientFundsError(self._balance, amount)

        self._balance -= amount
        self._record_transaction(TransactionType.WITHDRAWAL, amount, "Withdrawal")
        self._apply_transaction_fee()

    def _apply_transaction_fee(self) -> None:
        """Apply transaction fee if free transactions are exceeded."""
        self._monthly_transactions += 1

        if self._monthly_transactions > self.free_transactions and self.transaction_fee > 0:
            self._balance -= self.transaction_fee
            self._record_transaction(
                TransactionType.FEE,
                self.transaction_fee,
                f"Transaction fee ({self._monthly_transactions} transactions)"
            )

    def reset_monthly_transactions(self) -> None:
        """Reset monthly transaction counter."""
        self._monthly_transactions = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert account to dictionary."""
        data = super().to_dict()
        data.update({
            "overdraft_limit": self.overdraft_limit,
            "transaction_fee": self.transaction_fee,
            "free_transactions": self.free_transactions,
            "monthly_transactions": self._monthly_transactions,
        })
        return data


class SavingsAccount(BankAccount):
    """
    Savings account with interest calculation and minimum balance requirements.

    Attributes:
        interest_rate: Annual interest rate (as decimal)
        minimum_balance: Minimum balance required
        withdrawal_limit: Maximum number of withdrawals per month
    """

    def __init__(
        self,
        account_number: str,
        account_holder: str,
        initial_balance: float = 0.0,
        interest_rate: float = 0.02,
        minimum_balance: float = 100.0,
        withdrawal_limit: int = 6,
    ):
        super().__init__(account_number, account_holder, initial_balance)
        self.interest_rate = interest_rate
        self.minimum_balance = minimum_balance
        self.withdrawal_limit = withdrawal_limit
        self._monthly_withdrawals = 0

    def deposit(self, amount: float) -> None:
        """Deposit money into the savings account."""
        if amount <= 0:
            raise InvalidAmountError(amount, "Deposit amount must be positive")

        self._balance += amount
        self._record_transaction(TransactionType.DEPOSIT, amount, "Deposit")

    def withdraw(self, amount: float) -> None:
        """Withdraw money from the savings account."""
        if amount <= 0:
            raise InvalidAmountError(amount, "Withdrawal amount must be positive")

        if amount > self._balance:
            raise InsufficientFundsError(self._balance, amount)

        if self._balance - amount < self.minimum_balance:
            raise MinimumBalanceError(self._balance - amount, self.minimum_balance)

        if self._monthly_withdrawals >= self.withdrawal_limit:
            raise BankingException(
                f"Monthly withdrawal limit ({self.withdrawal_limit}) exceeded"
            )

        self._balance -= amount
        self._monthly_withdrawals += 1
        self._record_transaction(
            TransactionType.WITHDRAWAL,
            amount,
            f"Withdrawal ({self._monthly_withdrawals}/{self.withdrawal_limit})"
        )

    def add_interest(self) -> float:
        """
        Calculate and add interest to the account balance.

        Returns:
            Amount of interest added
        """
        interest = self._balance * self.interest_rate
        self._balance += interest
        self._record_transaction(
            TransactionType.INTEREST,
            interest,
            f"Interest at {self.interest_rate * 100:.2f}%"
        )
        return interest

    def reset_monthly_withdrawals(self) -> None:
        """Reset monthly withdrawal counter."""
        self._monthly_withdrawals = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert account to dictionary."""
        data = super().to_dict()
        data.update({
            "interest_rate": self.interest_rate,
            "minimum_balance": self.minimum_balance,
            "withdrawal_limit": self.withdrawal_limit,
            "monthly_withdrawals": self._monthly_withdrawals,
        })
        return data


class BusinessAccount(BankAccount):
    """
    Business account with transaction history and monthly statements.

    Attributes:
        business_name: Name of the business
        tax_id: Business tax identification number
        monthly_fee: Monthly maintenance fee
    """

    def __init__(
        self,
        account_number: str,
        account_holder: str,
        business_name: str,
        tax_id: str,
        initial_balance: float = 0.0,
        monthly_fee: float = 10.0,
    ):
        super().__init__(account_number, account_holder, initial_balance)
        self.business_name = business_name
        self.tax_id = tax_id
        self.monthly_fee = monthly_fee

    def deposit(self, amount: float) -> None:
        """Deposit money into the business account."""
        if amount <= 0:
            raise InvalidAmountError(amount, "Deposit amount must be positive")

        self._balance += amount
        self._record_transaction(TransactionType.DEPOSIT, amount, "Business deposit")

    def withdraw(self, amount: float) -> None:
        """Withdraw money from the business account."""
        if amount <= 0:
            raise InvalidAmountError(amount, "Withdrawal amount must be positive")

        if amount > self._balance:
            raise InsufficientFundsError(self._balance, amount)

        self._balance -= amount
        self._record_transaction(TransactionType.WITHDRAWAL, amount, "Business withdrawal")

    def charge_monthly_fee(self) -> None:
        """Charge the monthly maintenance fee."""
        if self._balance >= self.monthly_fee:
            self._balance -= self.monthly_fee
            self._record_transaction(
                TransactionType.FEE,
                self.monthly_fee,
                "Monthly maintenance fee"
            )

    def to_dict(self) -> Dict[str, Any]:
        """Convert account to dictionary."""
        data = super().to_dict()
        data.update({
            "business_name": self.business_name,
            "tax_id": self.tax_id,
            "monthly_fee": self.monthly_fee,
        })
        return data

    def __str__(self) -> str:
        """String representation of the business account."""
        return (
            f"{self.get_account_type()}: {self.account_number} | "
            f"Business: {self.business_name} | "
            f"Holder: {self.account_holder} | "
            f"Balance: ${self._balance:.2f}"
        )


# Import BankingException for BusinessAccount
from bank_management.exceptions import BankingException
