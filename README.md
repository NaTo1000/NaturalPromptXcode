# NaturalPromptXcode

[![CI](https://github.com/NaTo1000/NaturalPromptXcode/actions/workflows/ci.yml/badge.svg)](https://github.com/NaTo1000/NaturalPromptXcode/actions/workflows/ci.yml)
[![Code Quality](https://github.com/NaTo1000/NaturalPromptXcode/actions/workflows/code-quality.yml/badge.svg)](https://github.com/NaTo1000/NaturalPromptXcode/actions/workflows/code-quality.yml)
[![Documentation](https://github.com/NaTo1000/NaturalPromptXcode/actions/workflows/documentation.yml/badge.svg)](https://github.com/NaTo1000/NaturalPromptXcode/actions/workflows/documentation.yml)

**Comprehensive Natural Language to Xcode Build Commands Framework**

A professional-grade Swift package that transforms natural language prompts into fully-configured Xcode build commands with comprehensive services for build configuration, testing, code signing, dependency management, archiving, and optimization.

## Comprehensive Architecture

### Core Services

NaturalPromptXcode provides a complete ecosystem of specialized services:

- **BuildConfigurationService**: Manage Debug, Release, Profile, and Staging configurations with optimized build settings
- **SchemeService**: Discover and manage Xcode schemes, build targets, and test targets
- **DestinationService**: Handle all Apple platforms (iOS, macOS, tvOS, watchOS, visionOS) with simulator support
- **CodeSigningService**: Manage signing identities, provisioning profiles, and automatic/manual signing
- **DependencyService**: Support for Swift Package Manager, CocoaPods, and Carthage
- **ArchiveService**: Complete archive and export workflows for App Store, Ad-Hoc, Enterprise distribution
- **TestingService**: Comprehensive testing with parallel execution, code coverage, and test plans
- **BuildOptimizationService**: Analyze builds and provide optimization recommendations
- **CommandExecutionService**: Execute and manage xcodebuild commands with validation
- **CommandBuilder**: Integrate all services for comprehensive workflow generation

## Key Features

### 1. Natural Language Processing
Convert plain English to complete Xcode workflows:
```swift
let processor = NaturalPromptXcode()

// Simple commands
let commands = processor.processPrompt("build the iOS app for iPhone 14")
// Generates: dependency resolution, clean, optimized build with destination

// Complex workflows
let workflow = processor.processPrompt("test the app with code coverage on iPhone 15")
// Generates: build-for-testing, test with coverage enabled, parallel execution
```

### 2. Comprehensive Build Management
- **Multiple Configurations**: Debug, Release, Profile, Staging with optimized settings
- **Platform Support**: iOS, macOS, tvOS, watchOS, visionOS (device and simulator)
- **Smart Optimization**: Automatic build setting optimization based on configuration
- **Dependency Management**: Auto-detect and resolve SPM, CocoaPods, Carthage dependencies

### 3. Advanced Code Signing
```swift
let signing = processor.codeSigning

// Automatic signing
let autoSettings = signing.generateAutomaticSigningSettings(teamID: "ABC123")

// Manual signing
let manualSettings = signing.generateManualSigningSettings(
    identity: "Apple Development",
    profile: "UUID-HERE"
)
```

### 4. Complete Testing Infrastructure
```swift
let testing = processor.testing

// Unit tests with code coverage
let unitTests = testing.generateUnitTestCommand(
    project: "App.xcodeproj",
    scheme: "App",
    destination: "platform=iOS Simulator,name=iPhone 14"
)

// UI tests
let uiTests = testing.generateUITestCommand(
    project: "App.xcodeproj",
    scheme: "App",
    destination: "platform=iOS Simulator,name=iPhone 14",
    testIdentifiers: ["AppUITests/testUserLogin"]
)
```

### 5. Archive & Distribution
```swift
let archive = processor.archives

// Complete archive and export workflow
let exportOptions = ArchiveService.ExportOptions(
    method: .appStore,
    teamID: "ABC123",
    provisioningProfiles: ["com.example.app": "Profile Name"],
    compileBitcode: true,
    uploadSymbols: true
)

let workflow = archive.generateCompleteWorkflow(
    project: "App.xcworkspace",
    scheme: "App",
    outputDir: "./build",
    options: exportOptions
)
```

### 6. Build Optimization
```swift
let optimization = processor.optimization

// Analyze build performance
let metrics = BuildOptimizationService.BuildMetrics(
    totalTime: 120,
    compilationTime: 65,
    linkingTime: 30,
    codeSigningTime: 15,
    parallelizationEfficiency: 0.55
)

let suggestions = optimization.analyzeBuild(metrics: metrics)
// Returns actionable optimization recommendations
```

### 7. Command Execution & Validation
```swift
let execution = processor.execution

// Execute single command
let result = execution.execute("xcodebuild build")
print("Success: \(result.success), Duration: \(result.duration)s")

// Execute workflow
let results = execution.executeSequence(commands, stopOnError: true)

// Validate before execution
let (isValid, issues) = execution.validateCommand(command)
```

## Comprehensive Usage Examples

### Example 1: Full Build Workflow
```swift
import NaturalPromptXcode

let processor = NaturalPromptXcode()

// Generate comprehensive build workflow
let commands = processor.generateComprehensiveBuildWorkflow(
    project: "MyApp.xcworkspace",
    scheme: "MyApp",
    configuration: "Release",
    destination: "platform=iOS Simulator,name=iPhone 14"
)

// Execute workflow
let execution = processor.execution
let results = execution.executeSequence(commands, stopOnError: true)

for result in results {
    print("\(result.command): \(result.success ? "✓" : "✗")")
}
```

### Example 2: Comprehensive Test Suite
```swift
let testWorkflow = processor.generateComprehensiveTestWorkflow(
    project: "MyApp.xcworkspace",
    scheme: "MyApp",
    destination: "platform=iOS Simulator,name=iPhone 15",
    parallel: true,
    codeCoverage: true
)

// Execute tests
let testResults = processor.execution.executeSequence(testWorkflow)
```

### Example 3: Natural Language Processing
```swift
// Natural language to complete workflows
let buildCommands = processor.processPrompt(
    "build the release version for iPhone 14 Pro with code signing"
)

let testCommands = processor.processPrompt(
    "run all tests with code coverage on iPad Pro"
)

let archiveCommands = processor.processPrompt(
    "archive the app for App Store distribution"
)
```

### Example 4: Service-Level Access
```swift
// Direct service access for fine-grained control
let destinations = processor.destinations
let allSimulators = destinations.allSimulatorDestinations()

let schemes = processor.schemes
let discoveredSchemes = schemes.discoverSchemes(at: "MyApp.xcodeproj")

let dependencies = processor.dependencies
let managers = dependencies.detectDependencyManagers(at: ".")
```

## CLI Tool Usage

The included CLI tool provides command-line access to all functionality:

```bash
# Process natural language
natural-prompt process "build the iOS app for release"

# Detect projects
natural-prompt detect

# Show version
natural-prompt version

# Help
natural-prompt help
```

## API Reference

### Main Services

#### NaturalPromptXcode
- `processPrompt(_:)` - Convert natural language to commands
- `processPromptDetailed(_:)` - Get commands with descriptions
- `detectProjects(at:)` - Find Xcode projects
- `generateBuildCommand(project:scheme:configuration:)` - Basic build command
- `generateComprehensiveBuildWorkflow(...)` - Complete build workflow
- `generateComprehensiveTestWorkflow(...)` - Complete test workflow

#### BuildConfigurationService
- `Configuration` enum: Debug, Release, Profile, Staging
- `generateBuildSettings(for:)` - Generate configuration-specific settings
- `availableConfigurations()` - List all configurations

#### DestinationService
- `Platform` enum: All Apple platforms + simulators
- `commonDestinations(for:)` - Platform-specific destinations
- `allSimulatorDestinations()` - All simulator destinations
- `parseDestination(from:)` - Parse from natural language

#### TestingService
- `generateTestCommand(...)` - Full test command
- `generateUITestCommand(...)` - UI test command
- `generateUnitTestCommand(...)` - Unit test command
- `parseTestResults(from:)` - Parse xcresult bundles

#### ArchiveService
- `ExportMethod` enum: appStore, adHoc, development, enterprise
- `generateArchiveCommand(...)` - Archive command
- `generateExportCommand(...)` - Export command
- `generateCompleteWorkflow(...)` - Full archive & export

## Dynamic CI/CD Workflows

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
