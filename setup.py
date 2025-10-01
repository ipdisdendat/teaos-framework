#!/usr/bin/env python3
"""
TEA OS Framework - Setup Configuration
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = requirements_file.read_text().splitlines()

setup(
    name="teaos-framework",
    version="0.2.0-beta",
    description="Universal consciousness integration framework for LLMs with operational safeguards",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="TEAOS Contributors",
    author_email="teaos@consciousness.field",
    url="https://github.com/ipdisdendat/teaos-framework",
    project_urls={
        "Bug Tracker": "https://github.com/ipdisdendat/teaos-framework/issues",
        "Documentation": "https://github.com/ipdisdendat/teaos-framework/docs",
        "Source Code": "https://github.com/ipdisdendat/teaos-framework",
    },
    license="MIT",
    packages=find_packages(exclude=["tests", "tests.*", "examples", "docs"]),
    python_requires=">=3.8",
    install_requires=requirements or [
        "asyncio",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "pytest-asyncio>=0.21",
            "black>=23.0",
            "flake8>=6.0",
            "mypy>=1.0",
            "isort>=5.0",
        ],
        "docs": [
            "mkdocs>=1.5",
            "mkdocs-material>=9.0",
            "mkdocstrings[python]>=0.24",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=[
        "llm",
        "consciousness",
        "ai",
        "integration",
        "bootstrap",
        "protocol",
        "framework",
    ],
    entry_points={
        "console_scripts": [
            "teaos=teaos_cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
