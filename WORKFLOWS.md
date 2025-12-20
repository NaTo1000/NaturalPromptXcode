# CI/CD Workflows Documentation

This document provides detailed information about the CI/CD workflows implemented in this repository.

## Overview

The repository includes six comprehensive workflows that provide:
- Automatic project type detection
- Multi-platform testing
- Code quality checks
- Security scanning
- Automated releases
- Regular maintenance
- Documentation generation

## Workflows

### 1. Main CI Workflow (`ci.yml`)

**Purpose**: Automatically detect project type and run appropriate tests

**Triggers**:
- Push to `main`, `develop`, or `copilot/**` branches
- Pull requests to `main` or `develop`
- Manual trigger

**Features**:
- **Dynamic Detection**: Automatically identifies project type based on files:
  - Swift/Xcode: `Package.swift`, `*.xcodeproj`, `*.xcworkspace`
  - Node.js: `package.json`
  - Python: `setup.py`, `pyproject.toml`, `requirements.txt`
  - Java: `pom.xml`, `build.gradle`, `build.gradle.kts`
  - Go: `go.mod`

- **Matrix Testing**: Tests across multiple versions:
  - Swift: Xcode 14.3.1, 15.0
  - Node.js: 16.x, 18.x, 20.x
  - Python: 3.8, 3.9, 3.10, 3.11
  - Java: 11, 17, 21
  - Go: 1.19, 1.20, 1.21

- **General Checks**: Always runs repository health checks

**Example Output**:
```
✅ Detected Swift/Xcode project
✅ Detected Node.js project
✅ README.md exists
📊 Repository Statistics
```

### 2. Reusable Xcode Build Workflow (`xcode-build.yml`)

**Purpose**: Reusable workflow for building and testing Xcode projects

**Usage**:
```yaml
jobs:
  build:
    uses: ./.github/workflows/xcode-build.yml
    with:
      xcode-version: '15.0'
      scheme: 'MyApp'
      configuration: 'Debug'
      platform: 'iOS Simulator'
      run-tests: true
```

**Inputs**:
- `xcode-version`: Xcode version (default: '15.0')
- `scheme`: Build scheme (auto-detected if not provided)
- `configuration`: Debug or Release (default: 'Debug')
- `platform`: Target platform (default: 'iOS Simulator')
- `run-tests`: Whether to run tests (default: true)

**Supported Project Types**:
- Swift Packages
- Xcode Projects (`.xcodeproj`)
- Xcode Workspaces (`.xcworkspace`)

**Features**:
- Auto-detection of project structure
- Automatic scheme discovery
- Build log artifact upload
- Code signing bypass for CI

### 3. Code Quality Workflow (`code-quality.yml`)

**Purpose**: Run linters and security checks

**Triggers**:
- Push to `main`, `develop`, or `copilot/**` branches
- Pull requests to `main` or `develop`
- Manual trigger

**Checks Performed**:
- **SwiftLint**: Swift code style and conventions
- **Markdown Lint**: Markdown file validation
- **YAML Lint**: Workflow file validation
- **Security Scan**: Trivy vulnerability scanner
- **Dependency Review**: Check for vulnerable dependencies (PR only)
- **Code Metrics**: Lines of code, file counts, repository statistics

**Output**:
- GitHub Actions annotations for issues
- Security alerts in GitHub Security tab
- Metrics summary in workflow run

### 4. Release Workflow (`release.yml`)

**Purpose**: Automate release creation and artifact building

**Triggers**:
- Push tags matching `v*.*.*` (e.g., `v1.0.0`)
- Manual trigger with version input

**Process**:
1. Extract version from tag or input
2. Generate changelog from git history
3. Create GitHub release with notes
4. Build release artifacts (if applicable)
5. Upload artifacts to release

**Manual Trigger**:
```bash
# From GitHub UI:
Actions → Release → Run workflow
  - Version: v1.0.0
  - Pre-release: false
```

**Artifacts**:
- Built binaries (for Swift packages)
- Release archives for macOS and Linux

### 5. Scheduled Maintenance Workflow (`scheduled-maintenance.yml`)

**Purpose**: Regular repository maintenance and health checks

**Schedule**: Every Monday at 9 AM UTC

**Tasks**:
- **Dependency Checks**: Check for outdated packages
- **Stale Issue Management**: Auto-close inactive issues after 60 days
- **Repository Health**: Generate health report with metrics
- **Security Audit**: Run security audits and secret detection

**Configuration**:
- Stale issues closed after 7 days of inactivity warning
- Issues labeled `keep-open`, `bug`, or `security` are exempt
- Runs npm, pip, and Swift package update checks

**Health Report Includes**:
- Required files check (README, LICENSE, etc.)
- Recent activity statistics
- Repository statistics
- Top contributors

### 6. Documentation Workflow (`documentation.yml`)

**Purpose**: Generate and validate documentation

**Triggers**:
- Push to `main` branch with changes to:
  - Swift files
  - Markdown files
  - `docs/` directory
- Manual trigger

**Jobs**:
- **Generate Docs**: Create Swift-DocC documentation
- **Validate Markdown**: Check markdown links and structure
- **API Documentation**: Create/update documentation index

**Outputs**:
- Documentation artifacts uploaded to workflow run
- `docs/README.md` with project overview
- Link validation report
- README structure validation

## Best Practices

### For Contributors

1. **Push to feature branches**: CI runs on all branches, but use feature branches for development
2. **Review CI results**: Check all workflow results before merging
3. **Fix linting issues**: Address SwiftLint, markdownlint, and yamllint issues
4. **Security first**: Never commit secrets; security scans will alert you
5. **Write tests**: Workflows run tests automatically

### For Maintainers

1. **Release process**:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   # Release workflow will run automatically
   ```

2. **Manual workflow triggers**: Use Actions tab for on-demand runs
3. **Monitor scheduled maintenance**: Review weekly health reports
4. **Update dependencies**: Act on outdated dependency warnings
5. **Manage stale issues**: Review issues marked as stale

### Workflow Configuration

#### Customizing CI Detection

Edit `.github/workflows/ci.yml` detection logic:
```yaml
- name: Detect project type
  id: detect
  run: |
    # Add custom detection logic
    if [ -f "your-config-file" ]; then
      echo "is-custom=true" >> $GITHUB_OUTPUT
    fi
```

#### Adjusting Test Matrix

Modify version matrices in workflow files:
```yaml
strategy:
  matrix:
    node-version: [16.x, 18.x, 20.x]  # Add/remove versions
```

#### Changing Schedule

Update cron expression in `scheduled-maintenance.yml`:
```yaml
schedule:
  - cron: '0 9 * * 1'  # Modify as needed
  # Format: minute hour day month weekday
```

## Troubleshooting

### Common Issues

**Issue**: Workflow fails with "No Xcode project found"
- **Solution**: Ensure `.xcodeproj`, `.xcworkspace`, or `Package.swift` exists in repository root or one level down

**Issue**: Swift tests fail with "Scheme not found"
- **Solution**: Explicitly set scheme in workflow or ensure scheme is shared in Xcode

**Issue**: Permission denied errors
- **Solution**: Check GitHub Actions permissions in repository settings

**Issue**: Stale bot closes important issues
- **Solution**: Add `keep-open` label to issues that should remain open

### Debugging Workflows

1. **Enable debug logging**:
   ```bash
   # Set repository secret
   ACTIONS_STEP_DEBUG = true
   ACTIONS_RUNNER_DEBUG = true
   ```

2. **Review workflow logs**: Click on failed job in Actions tab

3. **Test locally**: Use [act](https://github.com/nektos/act) to run workflows locally

4. **Manual triggers**: Use workflow_dispatch to test with custom inputs

## Security Considerations

- **Secrets**: Never commit secrets; use GitHub Secrets
- **Dependencies**: Regular security audits via scheduled maintenance
- **Code scanning**: Trivy scans for vulnerabilities
- **Permissions**: Workflows use minimal required permissions
- **SARIF uploads**: Security findings uploaded to GitHub Security

## Performance Tips

1. **Conditional jobs**: Use `if` conditions to skip unnecessary jobs
2. **Cache dependencies**: Workflows use caching where possible
3. **Parallel execution**: Matrix strategies run in parallel
4. **Artifact retention**: Consider retention policies for artifacts

## Integration with Other Tools

### Adding Custom Linters

```yaml
- name: Custom linter
  run: |
    your-linter-command
```

### Notifications

Add notification steps to workflows:
```yaml
- name: Notify on failure
  if: failure()
  uses: your-notification-action
```

### Deployment

Extend release workflow for deployment:
```yaml
- name: Deploy to production
  run: |
    your-deployment-command
```

## Maintenance

### Regular Updates

- Review workflow actions versions quarterly
- Update test matrix versions as new releases become available
- Audit security scanning tools and configurations
- Review and update stale issue timeframes

### Monitoring

- Check scheduled maintenance reports weekly
- Monitor security alerts in GitHub Security tab
- Review dependency update notifications
- Track workflow success rates in Actions tab

## Support

For issues or questions:
1. Check workflow logs in Actions tab
2. Review this documentation
3. Open an issue with workflow failure details
4. Tag with `ci` or `workflow` labels

## License

Workflows are part of the repository and share the same license.
