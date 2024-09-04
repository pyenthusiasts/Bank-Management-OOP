# Bank Management System - OOP Example

This project demonstrates an advanced Python implementation of a **Bank Management System** using Object-Oriented Programming (OOP) principles. The system allows users to create different types of bank accounts, deposit and withdraw money, view account details, and apply interest to savings accounts. It illustrates key OOP concepts such as inheritance, polymorphism, encapsulation, and exception handling.

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Examples](#examples)
6. [Contributing](#contributing)
7. [License](#license)

## Introduction

This project simulates a simple bank management system where users can perform operations on different types of accounts: **Checking Account** and **Savings Account**. Each account type has specific behaviors, such as adding interest for savings accounts, and adheres to a common interface defined by an abstract base class.

The system is designed to demonstrate core OOP principles in Python, making it an excellent reference for those learning or teaching object-oriented design.

## Features

- **Abstract Base Class (`BankAccount`)**: Defines a common interface for all types of bank accounts.
- **Checking Account (`CheckingAccount`)**: Allows deposits and withdrawals with basic functionality.
- **Savings Account (`SavingsAccount`)**: Supports deposits, withdrawals, and interest calculation.
- **Polymorphism**: Different account types implement the same methods in different ways.
- **Encapsulation**: The balance is managed internally and is not directly accessible from outside the class.
- **Exception Handling**: Ensures that all operations are valid and handles errors gracefully.

## Installation

### Prerequisites

- Python 3.x

### Install Required Packages

No external packages are required for this project.

## Usage

1. **Clone the Repository**:

   Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your-username/bank-management-system.git
   ```

2. **Navigate to the Directory**:

   Go to the project directory:

   ```bash
   cd bank-management-system
   ```

3. **Run the Script**:

   Run the script using Python:

   ```bash
   python bank_management_system.py
   ```

### Running the Program

When you run the script, it will:

- Create instances of `CheckingAccount` and `SavingsAccount`.
- Perform various operations (deposit, withdraw, add interest) on these accounts.
- Display account details before and after operations.

## Examples

### Output

Running the script will produce output similar to:

```
=== Checking Account Details ===
Account Number: CHK12345, Account Holder: John Doe, Balance: 500.00
Deposited $200.00 to Checking Account.
Withdrew $150.00 from Checking Account.
Updated Balance: 550.0

=== Savings Account Details ===
Account Number: SAV67890, Account Holder: Jane Doe, Balance: 1000.00
Deposited $300.00 to Savings Account.
Withdrew $100.00 from Savings Account.
Added interest of $36.00 to Savings Account.
Updated Balance: 1236.0
```

### Modifying the Code

To add a new type of bank account, you can create a new class that inherits from `BankAccount` and implement the required methods (`deposit` and `withdraw`). For example:

```python
class BusinessAccount(BankAccount):
    # Implement deposit and withdraw methods specific to BusinessAccount
    pass
```

## Contributing

Contributions are welcome! If you have ideas for new features, improvements, or bug fixes, please feel free to open an issue or create a pull request.

### Steps to Contribute

1. **Fork the Repository**: Click the 'Fork' button at the top right of this page.
2. **Clone Your Fork**: Clone your forked repository to your local machine.
   ```bash
   git clone https://github.com/your-username/bank-management-system.git
   ```
3. **Create a Branch**: Create a new branch for your feature or bug fix.
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make Changes**: Make your changes and commit them with a descriptive message.
   ```bash
   git commit -m "Add: feature description"
   ```
5. **Push Changes**: Push your changes to your forked repository.
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Create a Pull Request**: Go to the original repository on GitHub and create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Thank you for using the Bank Management System! If you have any questions or feedback, feel free to reach out. Happy coding! 😊
