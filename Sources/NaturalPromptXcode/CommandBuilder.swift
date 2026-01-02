import Foundation

/// Comprehensive command builder that integrates all services
public class CommandBuilder {
    
    private let configService: BuildConfigurationService
    private let schemeService: SchemeService
    private let destinationService: DestinationService
    private let signingService: CodeSigningService
    private let dependencyService: DependencyService
    private let archiveService: ArchiveService
    private let testingService: TestingService
    private let optimizationService: BuildOptimizationService
    
    /// Initialize command builder with all services
    public init() {
        self.configService = BuildConfigurationService()
        self.schemeService = SchemeService()
        self.destinationService = DestinationService()
        self.signingService = CodeSigningService()
        self.dependencyService = DependencyService()
        self.archiveService = ArchiveService()
        self.testingService = TestingService()
        self.optimizationService = BuildOptimizationService()
    }
    
    /// Build context containing all build parameters
    public struct BuildContext {
        public let projectPath: String
        public let scheme: String
        public let configuration: String
        public let destination: String?
        public let workingDirectory: String
        
        public init(
            projectPath: String,
            scheme: String,
            configuration: String = "Debug",
            destination: String? = nil,
            workingDirectory: String = "."
        ) {
            self.projectPath = projectPath
            self.scheme = scheme
            self.configuration = configuration
            self.destination = destination
            self.workingDirectory = workingDirectory
        }
    }
    
    /// Generate comprehensive build workflow
    /// - Parameter context: Build context
    /// - Returns: Array of commands to execute
    public func generateBuildWorkflow(context: BuildContext) -> [String] {
        var commands: [String] = []
        
        // 1. Dependency resolution
        let managers = dependencyService.detectDependencyManagers(at: context.workingDirectory)
        for manager in managers {
            commands.append(dependencyService.generateInstallCommand(for: manager))
        }
        
        // 2. Clean build folder (optional)
        commands.append("rm -rf DerivedData")
        
        // 3. Generate build command
        let projectFlag = context.projectPath.hasSuffix(".xcworkspace") ? "-workspace" : "-project"
        var buildCommand = "xcodebuild build \(projectFlag) \(context.projectPath) -scheme \(context.scheme) -configuration \(context.configuration)"
        
        if let destination = context.destination {
            buildCommand += " -destination '\(destination)'"
        }
        
        // 4. Add optimization settings
        let optimizedCommand = optimizationService.generateOptimizedCommand(
            baseCommand: buildCommand,
            buildType: context.configuration
        )
        
        commands.append(optimizedCommand)
        
        return commands
    }
    
    /// Generate comprehensive test workflow
    /// - Parameters:
    ///   - context: Build context
    ///   - testConfig: Test configuration
    /// - Returns: Array of test commands
    public func generateTestWorkflow(
        context: BuildContext,
        testConfig: TestingService.TestConfiguration
    ) -> [String] {
        var commands: [String] = []
        
        // 1. Build for testing
        let projectFlag = context.projectPath.hasSuffix(".xcworkspace") ? "-workspace" : "-project"
        commands.append("xcodebuild build-for-testing \(projectFlag) \(context.projectPath) -scheme \(context.scheme)")
        
        // 2. Run tests
        let testCommand = testingService.generateTestCommand(
            project: context.projectPath,
            scheme: context.scheme,
            destination: context.destination ?? "platform=iOS Simulator,name=iPhone 14",
            configuration: testConfig
        )
        commands.append(testCommand)
        
        return commands
    }
    
    /// Generate archive and export workflow
    /// - Parameters:
    ///   - context: Build context
    ///   - exportOptions: Export options
    ///   - outputDir: Output directory
    /// - Returns: Array of archive/export commands
    public func generateArchiveWorkflow(
        context: BuildContext,
        exportOptions: ArchiveService.ExportOptions,
        outputDir: String
    ) -> [String] {
        return archiveService.generateCompleteWorkflow(
            project: context.projectPath,
            scheme: context.scheme,
            outputDir: outputDir,
            options: exportOptions
        )
    }
    
    /// Parse natural language and generate appropriate workflow
    /// - Parameter naturalLanguage: Natural language description
    /// - Returns: Array of commands based on intent
    public func parseAndGenerateWorkflow(from naturalLanguage: String) -> [String] {
        let lowercased = naturalLanguage.lowercased()
        var commands: [String] = []
        
        // Detect project details from natural language
        let projectPath = "App.xcodeproj"
        let scheme = "App"
        var configuration = "Debug"
        
        // Parse configuration
        if lowercased.contains("release") {
            configuration = "Release"
        }
        
        // Parse destination
        var destination: String? = nil
        if let parsedDest = destinationService.parseDestination(from: naturalLanguage) {
            destination = parsedDest.destinationString
        }
        
        let context = BuildContext(
            projectPath: projectPath,
            scheme: scheme,
            configuration: configuration,
            destination: destination
        )
        
        // Determine intent and generate workflow
        if lowercased.contains("test") {
            let testConfig = TestingService.TestConfiguration(
                parallel: !lowercased.contains("sequential"),
                codeCoverage: lowercased.contains("coverage")
            )
            commands = generateTestWorkflow(context: context, testConfig: testConfig)
        } else if lowercased.contains("archive") || lowercased.contains("export") {
            let exportMethod: ArchiveService.ExportMethod = lowercased.contains("app store") ? .appStore : .development
            let exportOptions = ArchiveService.ExportOptions(
                method: exportMethod,
                teamID: nil,
                provisioningProfiles: [:]
            )
            commands = generateArchiveWorkflow(context: context, exportOptions: exportOptions, outputDir: "./build")
        } else {
            // Default to build
            commands = generateBuildWorkflow(context: context)
        }
        
        return commands
    }
}
