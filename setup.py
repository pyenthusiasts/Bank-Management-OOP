"""
Setup configuration for Bank Management System.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="bank-management-oop",
    version="2.0.0",
    author="Bank Management Team",
    author_email="info@bankmanagement.example.com",
    description="A comprehensive bank management system demonstrating OOP principles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pyenthusiasts/Bank-Management-OOP",
    packages=find_packages(exclude=["tests", "tests.*", "examples", "docs"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Topic :: Education",
        "Topic :: Office/Business :: Financial",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    install_requires=[
        # No external dependencies for core functionality
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.990",
            "isort>=5.10.0",
        ],
        "cli": [
            # Optional CLI enhancements
        ],
    },
    entry_points={
        "console_scripts": [
            "bank-cli=bank_management.cli:main",
        ],
    },
    keywords="bank banking oop object-oriented python education",
    project_urls={
        "Bug Reports": "https://github.com/pyenthusiasts/Bank-Management-OOP/issues",
        "Source": "https://github.com/pyenthusiasts/Bank-Management-OOP",
        "Documentation": "https://github.com/pyenthusiasts/Bank-Management-OOP/blob/main/README.md",
    },
)
