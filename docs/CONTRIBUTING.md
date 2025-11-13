# Contributing to Bank Management System

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/pyenthusiasts/Bank-Management-OOP.git
   cd Bank-Management-OOP
   ```

2. **Set up development environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install development dependencies
   pip install -e ".[dev]"
   ```

3. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### Code Style

We use several tools to maintain code quality:

- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

Run before committing:

```bash
# Format code
black bank_management tests

# Sort imports
isort bank_management tests

# Lint
flake8 bank_management

# Type check
mypy bank_management
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=bank_management

# Run specific test file
pytest tests/test_models.py

# Run specific test
pytest tests/test_models.py::TestCheckingAccount::test_deposit
```

### Writing Tests

- Write tests for all new features
- Maintain or improve code coverage
- Use descriptive test names
- Follow existing test patterns

Example:

```python
def test_new_feature(self):
    """Test description of what this test validates."""
    # Arrange
    account = CheckingAccount("CHK001", "Test User", 1000.0)

    # Act
    result = account.some_new_method()

    # Assert
    assert result == expected_value
```

## Commit Guidelines

### Commit Messages

Follow the conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:

```bash
git commit -m "feat(accounts): add credit card account type"
git commit -m "fix(storage): handle corrupted JSON files"
git commit -m "docs(api): update BankAccount documentation"
```

### Pull Requests

1. **Update documentation** if needed
2. **Add tests** for new features
3. **Ensure all tests pass**
4. **Update CHANGELOG** if applicable
5. **Write clear PR description**

PR Template:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe how you tested your changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] No new warnings
```

## Project Structure

```
Bank-Management-OOP/
├── bank_management/      # Main package
│   ├── __init__.py
│   ├── models.py        # Account models
│   ├── bank.py          # Bank management
│   ├── exceptions.py    # Custom exceptions
│   ├── storage.py       # Data persistence
│   ├── logger.py        # Logging config
│   └── cli.py           # CLI interface
├── tests/               # Test suite
│   ├── test_models.py
│   ├── test_bank.py
│   ├── test_storage.py
│   └── test_exceptions.py
├── examples/            # Example scripts
├── docs/                # Documentation
└── .github/             # GitHub workflows
```

## Adding New Features

### 1. New Account Type

To add a new account type:

1. Create class in `bank_management/models.py`:
   ```python
   class CreditCardAccount(BankAccount):
       def __init__(self, ...):
           super().__init__(...)
           # Add credit card specific attributes

       def deposit(self, amount):
           # Implement deposit logic

       def withdraw(self, amount):
           # Implement withdrawal logic
   ```

2. Add to `Bank.create_account()` in `bank_management/bank.py`
3. Write tests in `tests/test_models.py`
4. Update documentation

### 2. New Exception

1. Add to `bank_management/exceptions.py`:
   ```python
   class NewException(BankingException):
       """Description of when this is raised."""
       def __init__(self, ...):
           super().__init__(...)
   ```

2. Export in `__init__.py`
3. Write tests in `tests/test_exceptions.py`

### 3. New Bank Method

1. Add method to `Bank` class
2. Write comprehensive tests
3. Update API documentation
4. Add usage example if complex

## Documentation

Update documentation when:

- Adding new features
- Changing APIs
- Fixing bugs that affect usage
- Adding examples

Documentation locations:
- API reference: `docs/API.md`
- Usage guide: `docs/USAGE.md`
- README: `README.md`
- Docstrings: In code

## Code Review Process

1. Automated checks must pass:
   - All tests pass
   - Code style checks pass
   - No linting errors
   - Coverage maintained

2. Manual review focuses on:
   - Code quality and readability
   - Test coverage
   - Documentation
   - Breaking changes

## Release Process

1. Update version in `setup.py` and `__init__.py`
2. Update `CHANGELOG.md`
3. Create release PR
4. After merge, create GitHub release
5. Automated workflow publishes to PyPI

## Getting Help

- **Issues**: Open an issue for bugs or feature requests
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Check `docs/` directory

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

## Recognition

Contributors will be recognized in:
- README contributors section
- Release notes
- Project documentation

Thank you for contributing!
