import Foundation

/// Main library for natural language prompt to Xcode build commands with comprehensive services
public struct NaturalPromptXcode {
    /// The version of the library
    public static let version = "1.0.0"
    
    // Service instances
    private let commandBuilder: CommandBuilder
    private let configService: BuildConfigurationService
    private let schemeService: SchemeService
    private let destinationService: DestinationService
    private let signingService: CodeSigningService
    private let dependencyService: DependencyService
    private let archiveService: ArchiveService
    private let testingService: TestingService
    private let optimizationService: BuildOptimizationService
    private let executionService: CommandExecutionService
    
    /// Initialize a new NaturalPromptXcode instance with all services
    public init() {
        self.commandBuilder = CommandBuilder()
        self.configService = BuildConfigurationService()
        self.schemeService = SchemeService()
        self.destinationService = DestinationService()
        self.signingService = CodeSigningService()
        self.dependencyService = DependencyService()
        self.archiveService = ArchiveService()
        self.testingService = TestingService()
        self.optimizationService = BuildOptimizationService()
        self.executionService = CommandExecutionService()
    }
    
    /// Access to build configuration service
    public var buildConfiguration: BuildConfigurationService { configService }
    
    /// Access to scheme service
    public var schemes: SchemeService { schemeService }
    
    /// Access to destination service
    public var destinations: DestinationService { destinationService }
    
    /// Access to code signing service
    public var codeSigning: CodeSigningService { signingService }
    
    /// Access to dependency service
    public var dependencies: DependencyService { dependencyService }
    
    /// Access to archive service
    public var archives: ArchiveService { archiveService }
    
    /// Access to testing service
    public var testing: TestingService { testingService }
    
    /// Access to optimization service
    public var optimization: BuildOptimizationService { optimizationService }
    
    /// Access to execution service
    public var execution: CommandExecutionService { executionService }
    
    /// Process a natural language prompt and convert it to Xcode build commands
    /// - Parameter prompt: The natural language prompt describing what to build
    /// - Returns: An array of Xcode build commands
    public func processPrompt(_ prompt: String) -> [String] {
        // Use comprehensive command builder for natural language processing
        return commandBuilder.parseAndGenerateWorkflow(from: prompt)
    }
    
    /// Process prompt with detailed workflow
    /// - Parameter prompt: Natural language prompt
    /// - Returns: Detailed array of commands with explanations
    public func processPromptDetailed(_ prompt: String) -> [(command: String, description: String)] {
        let commands = processPrompt(prompt)
        return commands.enumerated().map { index, command in
            var description = ""
            if command.contains("resolve") || command.contains("install") || command.contains("update") {
                description = "Installing dependencies"
            } else if command.contains("rm -rf") {
                description = "Cleaning build artifacts"
            } else if command.contains("build-for-testing") {
                description = "Building for testing"
            } else if command.contains("test") {
                description = "Running tests"
            } else if command.contains("archive") {
                description = "Creating archive"
            } else if command.contains("exportArchive") {
                description = "Exporting archive"
            } else if command.contains("build") {
                description = "Building project"
            } else {
                description = "Executing step \(index + 1)"
            }
            return (command, description)
        }
    }
    
    /// Detect available Xcode projects in a directory
    /// - Parameter path: The directory path to search
    /// - Returns: An array of detected project files
    public func detectProjects(at path: String = ".") -> [String] {
        var projects: [String] = []
        
        let fileManager = FileManager.default
        
        do {
            let items = try fileManager.contentsOfDirectory(atPath: path)
            
            for item in items {
                if item.hasSuffix(".xcodeproj") {
                    projects.append(item)
                } else if item.hasSuffix(".xcworkspace") {
                    projects.append(item)
                }
            }
        } catch {
            print("Error detecting projects: \(error)")
        }
        
        return projects
    }
    
    /// Generate a complete build command with project and scheme
    /// - Parameters:
    ///   - project: The project or workspace file
    ///   - scheme: The scheme to build
    ///   - configuration: The build configuration (Debug or Release)
    /// - Returns: A complete xcodebuild command
    public func generateBuildCommand(
        project: String,
        scheme: String,
        configuration: String = "Debug"
    ) -> String {
        let projectFlag = project.hasSuffix(".xcworkspace") ? "-workspace" : "-project"
        return "xcodebuild \(projectFlag) \(project) -scheme \(scheme) -configuration \(configuration) build"
    }
    
    /// Generate comprehensive build workflow with all steps
    /// - Parameters:
    ///   - project: Project path
    ///   - scheme: Scheme name
    ///   - configuration: Build configuration
    ///   - destination: Build destination
    /// - Returns: Complete workflow commands
    public func generateComprehensiveBuildWorkflow(
        project: String,
        scheme: String,
        configuration: String = "Debug",
        destination: String? = nil
    ) -> [String] {
        let context = CommandBuilder.BuildContext(
            projectPath: project,
            scheme: scheme,
            configuration: configuration,
            destination: destination
        )
        return commandBuilder.generateBuildWorkflow(context: context)
    }
    
    /// Generate comprehensive test workflow
    /// - Parameters:
    ///   - project: Project path
    ///   - scheme: Scheme name
    ///   - destination: Test destination
    ///   - parallel: Run tests in parallel
    ///   - codeCoverage: Enable code coverage
    /// - Returns: Complete test workflow commands
    public func generateComprehensiveTestWorkflow(
        project: String,
        scheme: String,
        destination: String = "platform=iOS Simulator,name=iPhone 14",
        parallel: Bool = true,
        codeCoverage: Bool = true
    ) -> [String] {
        let context = CommandBuilder.BuildContext(
            projectPath: project,
            scheme: scheme,
            configuration: "Debug",
            destination: destination
        )
        let testConfig = TestingService.TestConfiguration(
            parallel: parallel,
            codeCoverage: codeCoverage
        )
        return commandBuilder.generateTestWorkflow(context: context, testConfig: testConfig)
    }
}
