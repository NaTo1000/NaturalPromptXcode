# Getting Started

Welcome to NaturalPromptXcode! This guide will help you get up and running with building iOS apps from natural language prompts.

## Prerequisites

Before you begin, ensure you have the following installed:

- **macOS**: Version 12.0 or later
- **Xcode**: Version 14.0 or later
- **Python**: Version 3.9 or later
- **Git**: For version control

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/NaTo1000/NaturalPromptXcode.git
cd NaturalPromptXcode
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure AI Model

Set up your AI model credentials (if using external APIs):

```bash
export OPENAI_API_KEY="your-api-key-here"
```

Or configure local model settings in `config.yaml`.

## Quick Start

### Example 1: Simple Counter App

```bash
python naturalpromptxcode.py "Create a simple counter app with increment and decrement buttons"
```

### Example 2: Weather App

```bash
python naturalpromptxcode.py "Build a weather app that shows current temperature and conditions"
```

## Project Structure

```
NaturalPromptXcode/
├── docs/           # Documentation
├── src/            # Source code
│   ├── nlp/       # Natural language processing
│   ├── codegen/   # Code generation
│   └── builder/   # Project building
├── models/         # AI model configurations
└── examples/       # Example projects
```

## Next Steps

- Read the [Architecture Overview](ARCHITECTURE.md)
- Check out the [API Reference](API_REFERENCE.md)
- Learn about [Contributing](CONTRIBUTING.md)
- Explore example prompts in the `examples/` directory

## Troubleshooting

### Common Issues

**Issue**: "Xcode command line tools not found"
**Solution**: Run `xcode-select --install`

**Issue**: "AI model API key not configured"
**Solution**: Set your API key in environment variables or config file

**Issue**: "Build failed"
**Solution**: Ensure Xcode is properly installed and you have accepted the license

## Support

For issues and questions:
- Open an issue on GitHub
- Check the documentation in `docs/`
- Review example projects
