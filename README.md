# NaturalPromptXcode

[![CI](https://github.com/NaTo1000/NaturalPromptXcode/actions/workflows/ci.yml/badge.svg)](https://github.com/NaTo1000/NaturalPromptXcode/actions/workflows/ci.yml)
[![Code Quality](https://github.com/NaTo1000/NaturalPromptXcode/actions/workflows/code-quality.yml/badge.svg)](https://github.com/NaTo1000/NaturalPromptXcode/actions/workflows/code-quality.yml)
[![Documentation](https://github.com/NaTo1000/NaturalPromptXcode/actions/workflows/documentation.yml/badge.svg)](https://github.com/NaTo1000/NaturalPromptXcode/actions/workflows/documentation.yml)

Natural language prompt to code for Xcode building commands to create the future.

## Features

- 🚀 Dynamic CI/CD workflows with automatic project type detection
- 🔍 Code quality checks and security scanning
- 📦 Automated release management
- 📊 Code metrics and repository health monitoring
- 🔄 Scheduled maintenance and dependency checks
- 📚 Automatic documentation generation

## CI/CD Workflows

This repository includes comprehensive CI/CD workflows that automatically detect and test different project types:

### Main CI Workflow (`ci.yml`)

The main CI workflow automatically detects your project type and runs appropriate tests:

- **Swift/Xcode Projects**: Builds and tests with multiple Xcode versions
- **Node.js Projects**: Tests across Node.js 16, 18, and 20
- **Python Projects**: Tests across Python 3.8, 3.9, 3.10, and 3.11
- **Java Projects**: Supports Maven and Gradle builds with Java 11, 17, and 21
- **Go Projects**: Tests across Go 1.19, 1.20, and 1.21

The workflow runs on:
- Push to `main`, `develop`, or `copilot/**` branches
- Pull requests to `main` or `develop`
- Manual trigger via workflow_dispatch

### Reusable Xcode Build Workflow (`xcode-build.yml`)

A reusable workflow for building Xcode projects with configurable options:

```yaml
uses: ./.github/workflows/xcode-build.yml
with:
  xcode-version: '15.0'
  configuration: 'Debug'
  platform: 'iOS Simulator'
  run-tests: true
```

Supports:
- Swift Packages
- Xcode Projects
- Xcode Workspaces
- Multiple platforms (iOS, macOS, tvOS, watchOS)

### Code Quality Workflow (`code-quality.yml`)

Runs linters and security checks:
- SwiftLint for Swift code
- Markdown linting
- YAML validation
- Security scanning with Trivy
- Dependency review
- Code metrics reporting

### Release Workflow (`release.yml`)

Automates release creation:
- Triggered by version tags (e.g., `v1.0.0`)
- Generates changelog from commits
- Builds release artifacts
- Creates GitHub releases

### Scheduled Maintenance (`scheduled-maintenance.yml`)

Runs weekly maintenance tasks:
- Dependency update checks
- Stale issue management
- Repository health reports
- Security audits

### Documentation Workflow (`documentation.yml`)

Generates and validates documentation:
- Swift-DocC documentation generation
- Markdown link validation
- README structure validation
- API documentation updates

## Usage

### For Xcode/Swift Projects

1. Add a `Package.swift` file or `.xcodeproj`/`.xcworkspace`
2. Push to your repository
3. Workflows will automatically detect and build your project

### For Other Project Types

The CI workflows automatically detect:
- `package.json` → Node.js workflow
- `requirements.txt` or `pyproject.toml` → Python workflow
- `pom.xml` or `build.gradle` → Java workflow
- `go.mod` → Go workflow

### Manual Workflow Triggers

All workflows can be manually triggered from the Actions tab:

1. Go to Actions → Select workflow
2. Click "Run workflow"
3. Choose branch and configure options

## Project Structure

```
.github/
  workflows/
    ci.yml                      # Main CI with auto-detection
    xcode-build.yml            # Reusable Xcode build
    code-quality.yml           # Code quality checks
    release.yml                # Release automation
    scheduled-maintenance.yml  # Weekly maintenance
    documentation.yml          # Documentation generation
```

## Contributing

Contributions are welcome! The CI workflows will automatically:
- Detect your project type
- Run appropriate tests
- Check code quality
- Validate documentation

## License

See LICENSE file for details.
