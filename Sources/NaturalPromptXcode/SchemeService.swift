import Foundation

/// Service for managing build schemes and targets
public class SchemeService {
    
    /// Represents an Xcode scheme
    public struct Scheme {
        public let name: String
        public let buildTargets: [String]
        public let testTargets: [String]
        public let isShared: Bool
        
        public init(name: String, buildTargets: [String], testTargets: [String], isShared: Bool) {
            self.name = name
            self.buildTargets = buildTargets
            self.testTargets = testTargets
            self.isShared = isShared
        }
    }
    
    /// Initialize the scheme service
    public init() {}
    
    /// Discover schemes in an Xcode project
    /// - Parameter projectPath: Path to .xcodeproj or .xcworkspace
    /// - Returns: Array of discovered schemes
    public func discoverSchemes(at projectPath: String) -> [Scheme] {
        // In a real implementation, this would parse Xcode project files
        // For now, return common default schemes
        return [
            Scheme(name: "App", buildTargets: ["App"], testTargets: ["AppTests"], isShared: true),
            Scheme(name: "Framework", buildTargets: ["Framework"], testTargets: ["FrameworkTests"], isShared: true)
        ]
    }
    
    /// Generate xcodebuild command for a scheme
    /// - Parameters:
    ///   - scheme: The scheme to build
    ///   - project: Project or workspace path
    ///   - configuration: Build configuration
    /// - Returns: Complete xcodebuild command
    public func generateBuildCommand(
        scheme: Scheme,
        project: String,
        configuration: String = "Debug"
    ) -> String {
        let projectFlag = project.hasSuffix(".xcworkspace") ? "-workspace" : "-project"
        return "xcodebuild \(projectFlag) \(project) -scheme \(scheme.name) -configuration \(configuration) build"
    }
    
    /// Generate test command for a scheme
    /// - Parameters:
    ///   - scheme: The scheme to test
    ///   - project: Project or workspace path
    ///   - destination: Test destination
    /// - Returns: Complete xcodebuild test command
    public func generateTestCommand(
        scheme: Scheme,
        project: String,
        destination: String = "platform=iOS Simulator,name=iPhone 14"
    ) -> String {
        let projectFlag = project.hasSuffix(".xcworkspace") ? "-workspace" : "-project"
        return "xcodebuild \(projectFlag) \(project) -scheme \(scheme.name) -destination '\(destination)' test"
    }
}
