# 🚀 NaturalPromptXcode

Build iOS applications directly from natural language prompts using AI-powered code generation.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

## ✨ Overview

NaturalPromptXcode revolutionizes iOS app development by transforming natural language descriptions into fully functional iOS applications. Whether you're a seasoned developer prototyping quickly or a newcomer exploring iOS development, NaturalPromptXcode makes app creation intuitive and accessible.

## 🎯 Features

- **Natural Language to Code**: Describe your app in plain English, get Swift code
- **SwiftUI & UIKit Support**: Generate modern SwiftUI or classic UIKit code
- **Instant Prototyping**: From idea to working app in seconds
- **Xcode Integration**: Generates complete, buildable Xcode projects
- **Customizable**: Configure AI models, output formats, and build settings
- **Extensible**: Built on a modular architecture for easy customization
- **Secure Releases**: SHA256 checksums and GPG signatures for artifact verification

## 📋 Prerequisites

- **macOS**: 12.0 or later
- **Xcode**: 14.0 or later (with Command Line Tools)
- **Python**: 3.9 or later
- **API Key**: OpenAI API key (or configure local LLM)

## 🔧 Installation

### Quick Install

```bash
# Clone the repository
git clone https://github.com/NaTo1000/NaturalPromptXcode.git
cd NaturalPromptXcode

# Install dependencies
pip install -r requirements.txt

# Set up your API key
export OPENAI_API_KEY="your-api-key-here"
```

### Development Install

```bash
# Install with development dependencies
pip install -r requirements-dev.txt

# Install in editable mode
pip install -e .
```

## 🎮 Quick Start

### Create Your First App

```bash
# Simple counter app
python naturalpromptxcode.py "Create a simple counter app with increment and decrement buttons"

# Todo list app
python naturalpromptxcode.py "Build a todo list app where users can add and complete tasks"

# Weather app
python naturalpromptxcode.py "Create a weather app that shows temperature and conditions"
```

### Advanced Usage

```bash
# Specify output directory and framework
python naturalpromptxcode.py "Create a photo gallery app" \
  --output-dir ~/Projects/PhotoApp \
  --ui-framework uikit \
  --verbose

# Generate without building (dry-run)
python naturalpromptxcode.py "Create a calculator app" --dry-run
```

## 📖 Documentation

Comprehensive documentation is available in the `docs/` directory:

- **[Getting Started Guide](docs/GETTING_STARTED.md)**: Complete setup and usage instructions
- **[Architecture Overview](docs/ARCHITECTURE.md)**: System design and components
- **[API Reference](docs/API_REFERENCE.md)**: Detailed API documentation
- **[Contributing Guide](docs/CONTRIBUTING.md)**: How to contribute to the project
- **[Security Guide](docs/SECURITY.md)**: SHA256 checksums and GPG signature verification

## 🏗️ Project Structure

```
NaturalPromptXcode/
├── docs/                   # Documentation
│   ├── ARCHITECTURE.md
│   ├── GETTING_STARTED.md
│   ├── API_REFERENCE.md
│   └── CONTRIBUTING.md
├── src/                    # Source code
│   ├── nlp/               # Natural language processing
│   ├── codegen/           # Code generation
│   ├── builder/           # Project building
│   ├── config.py          # Configuration management
│   └── main.py            # CLI entry point
├── models/                 # AI model configurations
│   ├── MODEL_REQUIREMENTS.md
│   ├── CONFIG_EXAMPLES.md
│   └── PROMPT_TEMPLATES.md
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🔬 Examples

### Counter App
```bash
python naturalpromptxcode.py "Create a counter app with increment and decrement buttons"
```

Generates a SwiftUI app with state management and button actions.

### Todo List
```bash
python naturalpromptxcode.py "Create a todo list where users can add, complete, and delete tasks"
```

Generates a list-based app with CRUD operations and state persistence.

### Weather Display
```bash
python naturalpromptxcode.py "Create a weather app showing temperature and conditions"
```

Generates an app with data display and icon representations.

## ⚙️ Configuration

Create a `config.yaml` file to customize behavior:

```yaml
model:
  provider: "openai"
  name: "gpt-4"
  temperature: 0.7

build:
  default_framework: "swiftui"
  target_ios_version: "15.0"

output:
  default_dir: "./output"
```

See [CONFIG_EXAMPLES.md](models/CONFIG_EXAMPLES.md) for more options.

## 🧪 Testing

```bash
# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Lint code
flake8 src/
black src/ --check
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Roadmap

- [ ] Enhanced NLP with GPT-4 integration
- [ ] Support for more complex app architectures
- [ ] Interactive UI designer
- [ ] Multi-platform support (macOS, watchOS)
- [ ] Automated testing generation
- [ ] CI/CD pipeline integration
- [ ] Plugin system for extensions

## 🙏 Acknowledgments

- Built with inspiration from the iOS developer community
- Powered by state-of-the-art language models
- Thanks to all contributors and supporters

## 📧 Contact

- **Project Repository**: [NaTo1000/NaturalPromptXcode](https://github.com/NaTo1000/NaturalPromptXcode)
- **Issues**: [GitHub Issues](https://github.com/NaTo1000/NaturalPromptXcode/issues)

---

**Made with ❤️ by the NaturalPromptXcode Team**

*Transforming ideas into iOS apps, one prompt at a time.*