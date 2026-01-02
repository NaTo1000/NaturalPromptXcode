import Foundation

/// Service for managing dependency management systems
public class DependencyService {
    
    /// Supported dependency managers
    public enum DependencyManager: String, CaseIterable {
        case swiftPackageManager = "Swift Package Manager"
        case cocoapods = "CocoaPods"
        case carthage = "Carthage"
        
        public var configFile: String {
            switch self {
            case .swiftPackageManager:
                return "Package.swift"
            case .cocoapods:
                return "Podfile"
            case .carthage:
                return "Cartfile"
            }
        }
    }
    
    /// Initialize the dependency service
    public init() {}
    
    /// Detect dependency managers in use
    /// - Parameter path: Project directory path
    /// - Returns: Array of detected dependency managers
    public func detectDependencyManagers(at path: String) -> [DependencyManager] {
        var managers: [DependencyManager] = []
        let fileManager = FileManager.default
        
        for manager in DependencyManager.allCases {
            let configPath = (path as NSString).appendingPathComponent(manager.configFile)
            if fileManager.fileExists(atPath: configPath) {
                managers.append(manager)
            }
        }
        
        return managers
    }
    
    /// Generate install command for dependency manager
    /// - Parameter manager: The dependency manager to use
    /// - Returns: Installation command
    public func generateInstallCommand(for manager: DependencyManager) -> String {
        switch manager {
        case .swiftPackageManager:
            return "swift package resolve"
        case .cocoapods:
            return "pod install"
        case .carthage:
            return "carthage update --platform iOS"
        }
    }
    
    /// Generate update command for dependency manager
    /// - Parameter manager: The dependency manager to use
    /// - Returns: Update command
    public func generateUpdateCommand(for manager: DependencyManager) -> String {
        switch manager {
        case .swiftPackageManager:
            return "swift package update"
        case .cocoapods:
            return "pod update"
        case .carthage:
            return "carthage update --platform iOS --use-xcframeworks"
        }
    }
    
    /// Generate build command that includes dependency resolution
    /// - Parameters:
    ///   - manager: The dependency manager to use
    ///   - buildCommand: The base build command
    /// - Returns: Complete command with dependency resolution
    public func generateBuildWithDependencies(
        manager: DependencyManager,
        buildCommand: String
    ) -> [String] {
        [generateInstallCommand(for: manager), buildCommand]
    }
}
