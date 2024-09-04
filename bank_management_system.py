from abc import ABC, abstractmethod

# Abstract Base Class for a bank account
class BankAccount(ABC):
    """
    A base class representing a generic bank account.

    Attributes:
    -----------
    account_number : str
        The unique account number.
    account_holder : str
        The name of the account holder.
    balance : float
        The current balance of the account.
    """

    def __init__(self, account_number, account_holder, initial_balance=0.0):
        self.account_number = account_number
        self.account_holder = account_holder
        self._balance = initial_balance  # Protected member to encapsulate balance

    @abstractmethod
    def deposit(self, amount):
        """Method to deposit money into the account."""
        pass

    @abstractmethod
    def withdraw(self, amount):
        """Method to withdraw money from the account."""
        pass

    def get_balance(self):
        """Returns the current balance of the account."""
        return self._balance

    def __str__(self):
        """Returns the account details as a string."""
        return f"Account Number: {self.account_number}, Account Holder: {self.account_holder}, Balance: {self._balance:.2f}"

# Concrete class for a Checking Account
class CheckingAccount(BankAccount):
    """
    A class representing a checking account, inherited from BankAccount.

    Methods:
    --------
    deposit(amount)
        Deposits money into the checking account.
    withdraw(amount)
        Withdraws money from the checking account.
    """

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._balance += amount
        print(f"Deposited ${amount:.2f} to Checking Account.")

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self._balance:
            raise ValueError("Insufficient funds.")
        self._balance -= amount
        print(f"Withdrew ${amount:.2f} from Checking Account.")

# Concrete class for a Savings Account
class SavingsAccount(BankAccount):
    """
    A class representing a savings account, inherited from BankAccount.

    Attributes:
    -----------
    interest_rate : float
        The interest rate for the savings account.

    Methods:
    --------
    deposit(amount)
        Deposits money into the savings account.
    withdraw(amount)
        Withdraws money from the savings account.
    add_interest()
        Adds interest to the balance based on the interest rate.
    """

    def __init__(self, account_number, account_holder, initial_balance=0.0, interest_rate=0.02):
        super().__init__(account_number, account_holder, initial_balance)
        self.interest_rate = interest_rate

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._balance += amount
        print(f"Deposited ${amount:.2f} to Savings Account.")

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self._balance:
            raise ValueError("Insufficient funds.")
        self._balance -= amount
        print(f"Withdrew ${amount:.2f} from Savings Account.")

    def add_interest(self):
        """Adds interest to the savings account based on the interest rate."""
        interest = self._balance * self.interest_rate
        self._balance += interest
        print(f"Added interest of ${interest:.2f} to Savings Account.")

# Main function to demonstrate the Bank Management System
def main():
    # Create instances of CheckingAccount and SavingsAccount
    checking_account = CheckingAccount(account_number="CHK12345", account_holder="John Doe", initial_balance=500.0)
    savings_account = SavingsAccount(account_number="SAV67890", account_holder="Jane Doe", initial_balance=1000.0, interest_rate=0.03)

    print("\n=== Checking Account Details ===")
    print(checking_account)
    checking_account.deposit(200.0)
    checking_account.withdraw(150.0)
    print("Updated Balance:", checking_account.get_balance())

    print("\n=== Savings Account Details ===")
    print(savings_account)
    savings_account.deposit(300.0)
    savings_account.withdraw(100.0)
    savings_account.add_interest()
    print("Updated Balance:", savings_account.get_balance())

if __name__ == "__main__":
    main()

