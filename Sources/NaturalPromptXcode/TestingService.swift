import Foundation

/// Service for testing and test automation
public class TestingService {
    
    /// Test configuration
    public struct TestConfiguration {
        public let testPlan: String?
        public let onlyTesting: [String]?
        public let skipTesting: [String]?
        public let parallel: Bool
        public let codeCoverage: Bool
        public let resultBundlePath: String?
        
        public init(
            testPlan: String? = nil,
            onlyTesting: [String]? = nil,
            skipTesting: [String]? = nil,
            parallel: Bool = true,
            codeCoverage: Bool = true,
            resultBundlePath: String? = nil
        ) {
            self.testPlan = testPlan
            self.onlyTesting = onlyTesting
            self.skipTesting = skipTesting
            self.parallel = parallel
            self.codeCoverage = codeCoverage
            self.resultBundlePath = resultBundlePath
        }
    }
    
    /// Test result
    public struct TestResult {
        public let totalTests: Int
        public let passedTests: Int
        public let failedTests: Int
        public let skippedTests: Int
        public let duration: TimeInterval
        public let codeCoveragePercentage: Double?
        
        public init(
            totalTests: Int,
            passedTests: Int,
            failedTests: Int,
            skippedTests: Int,
            duration: TimeInterval,
            codeCoveragePercentage: Double?
        ) {
            self.totalTests = totalTests
            self.passedTests = passedTests
            self.failedTests = failedTests
            self.skippedTests = skippedTests
            self.duration = duration
            self.codeCoveragePercentage = codeCoveragePercentage
        }
        
        public var success: Bool {
            failedTests == 0
        }
    }
    
    /// Initialize the testing service
    public init() {}
    
    /// Generate test command
    /// - Parameters:
    ///   - project: Project or workspace path
    ///   - scheme: Scheme to test
    ///   - destination: Test destination
    ///   - configuration: Test configuration
    /// - Returns: Complete xcodebuild test command
    public func generateTestCommand(
        project: String,
        scheme: String,
        destination: String,
        configuration: TestConfiguration
    ) -> String {
        let projectFlag = project.hasSuffix(".xcworkspace") ? "-workspace" : "-project"
        var command = "xcodebuild test \(projectFlag) \(project) -scheme \(scheme) -destination '\(destination)'"
        
        if let testPlan = configuration.testPlan {
            command += " -testPlan \(testPlan)"
        }
        
        if let onlyTesting = configuration.onlyTesting, !onlyTesting.isEmpty {
            let tests = onlyTesting.map { "-only-testing:\($0)" }.joined(separator: " ")
            command += " \(tests)"
        }
        
        if let skipTesting = configuration.skipTesting, !skipTesting.isEmpty {
            let tests = skipTesting.map { "-skip-testing:\($0)" }.joined(separator: " ")
            command += " \(tests)"
        }
        
        if configuration.parallel {
            command += " -parallel-testing-enabled YES"
        }
        
        if configuration.codeCoverage {
            command += " -enableCodeCoverage YES"
        }
        
        if let resultPath = configuration.resultBundlePath {
            command += " -resultBundlePath \(resultPath)"
        }
        
        return command
    }
    
    /// Generate UI test command
    /// - Parameters:
    ///   - project: Project path
    ///   - scheme: Scheme name
    ///   - destination: Test destination
    ///   - testIdentifiers: Specific UI tests to run
    /// - Returns: UI test command
    public func generateUITestCommand(
        project: String,
        scheme: String,
        destination: String,
        testIdentifiers: [String]?
    ) -> String {
        let config = TestConfiguration(
            onlyTesting: testIdentifiers,
            parallel: false,
            codeCoverage: false
        )
        return generateTestCommand(project: project, scheme: scheme, destination: destination, configuration: config)
    }
    
    /// Generate unit test command
    /// - Parameters:
    ///   - project: Project path
    ///   - scheme: Scheme name
    ///   - destination: Test destination
    /// - Returns: Unit test command
    public func generateUnitTestCommand(
        project: String,
        scheme: String,
        destination: String
    ) -> String {
        let config = TestConfiguration(
            parallel: true,
            codeCoverage: true
        )
        return generateTestCommand(project: project, scheme: scheme, destination: destination, configuration: config)
    }
    
    /// Generate test report from result bundle
    /// - Parameter resultBundlePath: Path to result bundle
    /// - Returns: Test result summary
    public func parseTestResults(from resultBundlePath: String) -> TestResult {
        // In a real implementation, this would parse the xcresult bundle
        // For now, return mock data
        return TestResult(
            totalTests: 100,
            passedTests: 95,
            failedTests: 5,
            skippedTests: 0,
            duration: 45.2,
            codeCoveragePercentage: 78.5
        )
    }
}
