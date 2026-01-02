# Contributing to NaturalPromptXcode

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Maintain professional communication

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported
2. Use the bug report template
3. Include:
   - Detailed description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Xcode version, Python version)
   - Error messages and logs

### Suggesting Features

1. Check existing feature requests
2. Clearly describe the feature and its benefits
3. Provide use cases
4. Consider implementation complexity

### Contributing Code

#### 1. Fork and Clone

```bash
git clone https://github.com/YOUR_USERNAME/NaturalPromptXcode.git
cd NaturalPromptXcode
```

#### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

#### 3. Make Changes

- Follow the coding style guide
- Write clear, concise commit messages
- Add tests for new features
- Update documentation as needed

#### 4. Test Your Changes

```bash
# Run unit tests
python -m pytest tests/

# Run linting
python -m pylint src/

# Test manually
python naturalpromptxcode.py "test prompt"
```

#### 5. Submit a Pull Request

- Push your branch to your fork
- Create a pull request with:
  - Clear title and description
  - Reference to related issues
  - Screenshots (if UI changes)
  - Test results

## Development Setup

### Install Development Dependencies

```bash
pip install -r requirements-dev.txt
```

### Run Tests

```bash
pytest tests/ -v
```

### Code Style

We follow PEP 8 for Python code:

```bash
# Format code
black src/

# Check style
flake8 src/
```

For Swift code, follow Apple's Swift Style Guide.

## Project Structure

```
src/
├── nlp/              # Natural language processing
│   ├── parser.py    # Prompt parsing
│   └── analyzer.py  # Requirement analysis
├── codegen/          # Code generation
│   ├── templates/   # Code templates
│   └── generator.py # Main generator
├── builder/          # Project building
│   └── xcode.py     # Xcode project management
└── main.py          # Entry point
```

## Coding Guidelines

### Python

- Use type hints
- Write docstrings for all public functions
- Maximum line length: 100 characters
- Use meaningful variable names

```python
def generate_code(prompt: str, framework: str = "swiftui") -> dict:
    """
    Generate iOS code from natural language prompt.
    
    Args:
        prompt: Natural language description
        framework: UI framework to use
        
    Returns:
        Dictionary containing generated code and metadata
    """
    pass
```

### Swift

- Use Swift 5.5+ features
- Follow SwiftUI best practices
- Write clear comments for complex logic

## Testing

### Unit Tests

```python
import pytest
from naturalpromptxcode import NaturalPromptXcode

def test_basic_generation():
    builder = NaturalPromptXcode()
    result = builder.validate_prompt("Create a counter app")
    assert result["valid"] == True
```

### Integration Tests

Test end-to-end workflows with real prompts.

## Documentation

- Update README.md for user-facing changes
- Update API_REFERENCE.md for API changes
- Add examples for new features
- Keep documentation in sync with code

## Review Process

1. Automated checks must pass (tests, linting)
2. Code review by maintainers
3. Address feedback and update PR
4. Approval and merge

## Release Process

Releases follow semantic versioning (MAJOR.MINOR.PATCH):

- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

## Getting Help

- Open an issue for questions
- Join discussions in GitHub Discussions
- Check existing documentation

## Recognition

Contributors are recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project README

Thank you for contributing to NaturalPromptXcode!
