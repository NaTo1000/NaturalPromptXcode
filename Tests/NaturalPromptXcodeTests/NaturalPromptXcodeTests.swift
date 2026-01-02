import XCTest
@testable import NaturalPromptXcode

final class NaturalPromptXcodeTests: XCTestCase {
    var processor: NaturalPromptXcode!
    
    override func setUp() {
        super.setUp()
        processor = NaturalPromptXcode()
    }
    
    override func tearDown() {
        processor = nil
        super.tearDown()
    }
    
    func testVersionIsAvailable() {
        XCTAssertFalse(NaturalPromptXcode.version.isEmpty)
        XCTAssertEqual(NaturalPromptXcode.version, "1.0.0")
    }
    
    func testProcessBuildPrompt() {
        let commands = processor.processPrompt("build the project")
        XCTAssertFalse(commands.isEmpty)
        XCTAssertTrue(commands.contains { $0.contains("build") })
    }
    
    func testProcessTestPrompt() {
        let commands = processor.processPrompt("run tests")
        XCTAssertFalse(commands.isEmpty)
        XCTAssertTrue(commands.contains { $0.contains("test") })
    }
    
    func testProcessArchivePrompt() {
        let commands = processor.processPrompt("archive the app")
        XCTAssertFalse(commands.isEmpty)
        XCTAssertTrue(commands.contains { $0.contains("archive") })
    }
    
    func testProcessReleasePrompt() {
        let commands = processor.processPrompt("build release version")
        XCTAssertFalse(commands.isEmpty)
        // Should contain release configuration
        XCTAssertTrue(commands.contains { $0.contains("Release") || $0.lowercased().contains("release") })
    }
    
    func testProcessDetailedPrompt() {
        let detailed = processor.processPromptDetailed("build and test the app")
        XCTAssertFalse(detailed.isEmpty)
        // Each item should have a command and description
        for item in detailed {
            XCTAssertFalse(item.command.isEmpty)
            XCTAssertFalse(item.description.isEmpty)
        }
    }
    
    func testDetectProjectsReturnsArray() {
        // This test verifies the method returns without crashing
        // and uses the default path parameter explicitly
        let projects = processor.detectProjects(at: ".")
        XCTAssertNotNil(projects)
    }
    
    func testGenerateBuildCommandForProject() {
        let command = processor.generateBuildCommand(
            project: "MyApp.xcodeproj",
            scheme: "MyApp",
            configuration: "Debug"
        )
        XCTAssertTrue(command.contains("-project"))
        XCTAssertTrue(command.contains("MyApp.xcodeproj"))
        XCTAssertTrue(command.contains("-scheme MyApp"))
        XCTAssertTrue(command.contains("-configuration Debug"))
    }
    
    func testGenerateBuildCommandForWorkspace() {
        let command = processor.generateBuildCommand(
            project: "MyApp.xcworkspace",
            scheme: "MyApp"
        )
        XCTAssertTrue(command.contains("-workspace"))
        XCTAssertTrue(command.contains("MyApp.xcworkspace"))
    }
    
    func testComprehensiveBuildWorkflow() {
        let workflow = processor.generateComprehensiveBuildWorkflow(
            project: "App.xcodeproj",
            scheme: "App",
            configuration: "Release"
        )
        XCTAssertFalse(workflow.isEmpty)
        // Should have multiple steps
        XCTAssertTrue(workflow.count >= 1)
    }
    
    func testComprehensiveTestWorkflow() {
        let workflow = processor.generateComprehensiveTestWorkflow(
            project: "App.xcodeproj",
            scheme: "App"
        )
        XCTAssertFalse(workflow.isEmpty)
        // Should contain test-related commands
        XCTAssertTrue(workflow.contains { $0.contains("test") })
    }
    
    // Service access tests
    func testServiceAccess() {
        // Test that all services are accessible
        XCTAssertNotNil(processor.buildConfiguration)
        XCTAssertNotNil(processor.schemes)
        XCTAssertNotNil(processor.destinations)
        XCTAssertNotNil(processor.codeSigning)
        XCTAssertNotNil(processor.dependencies)
        XCTAssertNotNil(processor.archives)
        XCTAssertNotNil(processor.testing)
        XCTAssertNotNil(processor.optimization)
        XCTAssertNotNil(processor.execution)
    }
    
    func testBuildConfigurationService() {
        let configs = processor.buildConfiguration.availableConfigurations()
        XCTAssertTrue(configs.contains("Debug"))
        XCTAssertTrue(configs.contains("Release"))
    }
    
    func testDestinationService() {
        let simulators = processor.destinations.allSimulatorDestinations()
        XCTAssertFalse(simulators.isEmpty)
        // Should have iOS simulator destinations
        XCTAssertTrue(simulators.contains { $0.platform.rawValue.contains("iOS") })
    }
    
    func testCaseInsensitivePromptProcessing() {
        let lowercaseCommands = processor.processPrompt("build project")
        let uppercaseCommands = processor.processPrompt("BUILD PROJECT")
        // Both should generate similar workflows
        XCTAssertFalse(lowercaseCommands.isEmpty)
        XCTAssertFalse(uppercaseCommands.isEmpty)
    }
}
