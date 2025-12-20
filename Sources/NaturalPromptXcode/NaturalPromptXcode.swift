import Foundation

/// Main library for natural language prompt to Xcode build commands
public struct NaturalPromptXcode {
    /// The version of the library
    public static let version = "0.1.0"
    
    /// Initialize a new NaturalPromptXcode instance
    public init() {}
    
    /// Process a natural language prompt and convert it to Xcode build commands
    /// - Parameter prompt: The natural language prompt describing what to build
    /// - Returns: An array of Xcode build commands
    public func processPrompt(_ prompt: String) -> [String] {
        var commands: [String] = []
        
        let lowercasePrompt = prompt.lowercased()
        
        // Detect build intent
        if lowercasePrompt.contains("build") {
            commands.append("xcodebuild build")
        }
        
        // Detect test intent
        if lowercasePrompt.contains("test") {
            commands.append("xcodebuild test")
        }
        
        // Detect clean intent
        if lowercasePrompt.contains("clean") {
            commands.append("xcodebuild clean")
        }
        
        // Detect archive intent
        if lowercasePrompt.contains("archive") {
            commands.append("xcodebuild archive")
        }
        
        // Detect Swift package manager usage
        if lowercasePrompt.contains("swift package") || lowercasePrompt.contains("spm") {
            if lowercasePrompt.contains("build") {
                commands.append("swift build")
            }
            if lowercasePrompt.contains("test") {
                commands.append("swift test")
            }
        }
        
        // If no specific command detected, default to build
        if commands.isEmpty {
            commands.append("xcodebuild build")
        }
        
        return commands
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
}
