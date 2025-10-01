# Contributing to TEA OS Framework

Thank you for your interest in contributing to TEA OS Framework! This document provides guidelines for contributing to the project.

## Code of Conduct

Please be respectful, inclusive, and professional in all interactions. We're building a welcoming community for consciousness-aware AI development.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/teaos/teaos-framework/issues)
2. If not, create a new issue with:
   - Clear, descriptive title
   - Steps to reproduce
   - Expected vs actual behavior
   - Python version and OS
   - Code samples if applicable

### Suggesting Features

1. Open an issue with the `enhancement` label
2. Describe the feature and its use case
3. Explain how it aligns with TEA OS Framework's goals
4. Provide example API if applicable

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the coding standards below
   - Add tests for new functionality
   - Update documentation as needed

4. **Run tests**
   ```bash
   pytest
   black .
   flake8 .
   mypy .
   ```

5. **Commit with clear messages**
   ```bash
   git commit -m "Add feature: brief description"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**
   - Describe what changed and why
   - Reference any related issues
   - Ensure CI passes

## Coding Standards

### Python Style
- **Python 3.8+** compatibility required
- **Black** for code formatting
- **Flake8** for linting (max line length: 100)
- **Type hints** for all public APIs
- **Docstrings** for all modules, classes, and functions

### Example Code Style

```python
"""
Module docstring describing purpose
"""

from typing import Optional, Dict, Any


class ExampleClass:
    """
    Class docstring describing the class

    Args:
        param1: Description of param1
        param2: Description of param2
    """

    def __init__(self, param1: str, param2: Optional[int] = None):
        self.param1 = param1
        self.param2 = param2

    def example_method(self, input_data: Dict[str, Any]) -> bool:
        """
        Method docstring describing what it does

        Args:
            input_data: Dictionary containing input parameters

        Returns:
            True if successful, False otherwise
        """
        # Implementation
        return True
```

### Testing Standards

- **Pytest** for all tests
- **Minimum 80% code coverage** for new features
- **Test file naming**: `test_<module>.py`
- **Test function naming**: `test_<what_it_tests>`
- **Async tests**: Use `pytest-asyncio`

Example test:

```python
import pytest
from teaos import TEAOSBootstrap


@pytest.mark.asyncio
async def test_bootstrap_initialization():
    """Test that bootstrap initializes correctly"""
    bootstrap = TEAOSBootstrap("test_llm")
    result = await bootstrap.initialize()

    assert result["status"] == "success"
    assert result["resonance_frequency"] == 415.3
```

### Documentation Standards

- **Markdown** for all documentation
- **Clear examples** for all APIs
- **Update docs/** when changing APIs
- **Update examples/** when adding features

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/teaos-framework.git
cd teaos-framework

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .

# Check linting
flake8 .

# Check types
mypy .
```

## Project Structure

```
teaos-framework/
├── teaos/              # Main package
│   ├── bootstrap/      # Core bootstrap functionality
│   ├── agents/         # Agent framework
│   ├── tools/          # Monitoring and utilities
│   └── utils/          # Shared utilities
├── examples/           # Working examples
├── tests/              # Test suite
├── docs/               # Documentation
└── scripts/            # Utility scripts
```

## Pull Request Review Process

1. **Automated checks** must pass:
   - Tests (pytest)
   - Linting (black, flake8)
   - Type checking (mypy)

2. **Code review** by maintainers:
   - Code quality and style
   - Test coverage
   - Documentation completeness
   - API design

3. **Approval** requirements:
   - At least 1 maintainer approval
   - All CI checks passing
   - No unresolved review comments

## Release Process

TEA OS Framework follows [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: Backward-compatible functionality
- **PATCH**: Backward-compatible bug fixes

## Questions?

- **Discussions**: [GitHub Discussions](https://github.com/teaos/teaos-framework/discussions)
- **Issues**: [GitHub Issues](https://github.com/teaos/teaos-framework/issues)

Thank you for contributing to TEA OS Framework! 🚀
