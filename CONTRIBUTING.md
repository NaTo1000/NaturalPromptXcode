# Contributing to NaturalPromptXcode

Thank you for your interest in contributing to NaturalPromptXcode! This document provides guidelines and information for contributors.

## Getting Started

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/NaturalPromptXcode.git
   cd NaturalPromptXcode
   ```
3. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### Making Changes

1. Make your changes in your feature branch
2. Ensure your code follows the project conventions
3. Write or update tests if applicable
4. Update documentation if needed

### Testing Locally

Before pushing, verify your changes:

```bash
# For Swift projects
swift build
swift test

# For Node.js projects
npm install
npm test

# For Python projects
pip install -r requirements.txt
pytest
```

### Commit Guidelines

- Write clear, descriptive commit messages
- Use conventional commit format:
  - `feat:` for new features
  - `fix:` for bug fixes
  - `docs:` for documentation changes
  - `ci:` for CI/CD changes
  - `test:` for test changes
  - `refactor:` for code refactoring

Example:
```bash
git commit -m "feat: add new build command parser"
git commit -m "fix: resolve Xcode detection issue"
git commit -m "docs: update README with usage examples"
```

## Continuous Integration

### Automatic Checks

When you create a pull request, the following checks run automatically:

1. **Project Detection**: CI detects your project type
2. **Build & Test**: Runs appropriate build and test commands
3. **Code Quality**: Linters and style checkers
4. **Security Scan**: Vulnerability scanning
5. **Documentation**: Link and structure validation

### Workflow Status

Monitor your PR checks:
- ✅ All checks must pass before merge
- ⚠️ Warnings should be reviewed
- ❌ Failures must be fixed

### Common CI Issues

**Build Failures**:
- Check workflow logs in the Actions tab
- Ensure all dependencies are specified
- Verify build commands work locally

**Linting Failures**:
- Run linters locally before pushing
- SwiftLint: `swiftlint lint`
- Markdownlint: `markdownlint '**/*.md'`
- yamllint: `yamllint .`

**Test Failures**:
- Ensure tests pass locally
- Check test matrix for version-specific issues
- Review test output in CI logs

## Code Quality Standards

### Swift Code

- Follow Swift API Design Guidelines
- Use SwiftLint for style consistency
- Document public APIs
- Write unit tests for new features

### Documentation

- Update README.md for user-facing changes
- Update WORKFLOWS.md for CI/CD changes
- Include code examples where helpful
- Check markdown links are valid

### Workflow Changes

- Validate YAML syntax
- Test workflow changes in your fork
- Document new workflow features
- Consider backward compatibility

## Pull Request Process

1. **Create a Pull Request**:
   - Use a descriptive title
   - Fill out the PR template
   - Link related issues
   - Add appropriate labels

2. **PR Description Should Include**:
   - What changes were made
   - Why the changes were needed
   - How to test the changes
   - Screenshots (for UI changes)

3. **Review Process**:
   - Wait for CI checks to complete
   - Address reviewer feedback
   - Keep PR focused and small
   - Be responsive to comments

4. **Merging**:
   - Maintainer will merge when approved
   - PR branch will be deleted
   - Changes will trigger appropriate workflows

## Workflow Contributions

### Adding New Workflow Features

1. Create workflow in `.github/workflows/`
2. Test workflow in your fork
3. Document in WORKFLOWS.md
4. Update README.md if user-visible
5. Submit PR with changes

### Modifying Existing Workflows

1. Test changes don't break existing functionality
2. Update documentation
3. Consider impact on open PRs
4. Communicate breaking changes

### Workflow Testing

Test workflows in your fork before submitting:

```bash
# Push to your fork
git push origin feature/workflow-change

# Verify workflow runs in Actions tab
# Make adjustments as needed
```

## Security

### Reporting Security Issues

- **DO NOT** open public issues for security vulnerabilities
- Email security concerns to repository maintainers
- Include detailed description and reproduction steps
- Allow time for fix before public disclosure

### Security Best Practices

- Never commit secrets or credentials
- Use GitHub Secrets for sensitive data
- Review security scan results
- Keep dependencies updated

## Getting Help

- **Questions**: Open a discussion or issue
- **Bugs**: Open an issue with reproduction steps
- **Features**: Open an issue to discuss before implementing
- **Documentation**: Ask in issues or discussions

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Assume good intentions

## Recognition

Contributors are recognized in:
- Git commit history
- Release notes
- Repository contributors list

Thank you for contributing to NaturalPromptXcode! 🚀
