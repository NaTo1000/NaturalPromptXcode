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
        XCTAssertEqual(NaturalPromptXcode.version, "0.1.0")
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
    
    func testProcessCleanPrompt() {
        let commands = processor.processPrompt("clean the project")
        XCTAssertFalse(commands.isEmpty)
        XCTAssertTrue(commands.contains { $0.contains("clean") })
    }
    
    func testProcessArchivePrompt() {
        let commands = processor.processPrompt("archive the app")
        XCTAssertFalse(commands.isEmpty)
        XCTAssertTrue(commands.contains { $0.contains("archive") })
    }
    
    func testProcessSwiftPackageBuildPrompt() {
        let commands = processor.processPrompt("swift package build")
        XCTAssertTrue(commands.contains("swift build"))
    }
    
    func testProcessSwiftPackageTestPrompt() {
        let commands = processor.processPrompt("swift package test")
        XCTAssertTrue(commands.contains("swift test"))
    }
    
    func testProcessEmptyPromptReturnsDefaultBuild() {
        let commands = processor.processPrompt("")
        XCTAssertFalse(commands.isEmpty)
        XCTAssertTrue(commands.contains { $0.contains("build") })
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
    
    func testDetectProjectsReturnsArray() {
        // This test just verifies the method returns without crashing
        let projects = processor.detectProjects()
        XCTAssertNotNil(projects)
    }
    
    func testProcessMultipleIntents() {
        let commands = processor.processPrompt("clean and build and test")
        XCTAssertTrue(commands.count >= 3)
        XCTAssertTrue(commands.contains { $0.contains("clean") })
        XCTAssertTrue(commands.contains { $0.contains("build") })
        XCTAssertTrue(commands.contains { $0.contains("test") })
    }
    
    func testCaseInsensitivePromptProcessing() {
        let lowercaseCommands = processor.processPrompt("build project")
        let uppercaseCommands = processor.processPrompt("BUILD PROJECT")
        XCTAssertEqual(lowercaseCommands, uppercaseCommands)
    }
}
