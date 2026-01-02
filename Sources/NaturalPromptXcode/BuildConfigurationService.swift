import Foundation

/// Service for managing Xcode build configurations
public class BuildConfigurationService {
    
    /// Available build configurations
    public enum Configuration: String, CaseIterable {
        case debug = "Debug"
        case release = "Release"
        case profile = "Profile"
        case staging = "Staging"
        
        public var buildSettings: [String: String] {
            switch self {
            case .debug:
                return [
                    "SWIFT_OPTIMIZATION_LEVEL": "-Onone",
                    "GCC_OPTIMIZATION_LEVEL": "0",
                    "DEBUG_INFORMATION_FORMAT": "dwarf-with-dsym",
                    "ENABLE_TESTABILITY": "YES"
                ]
            case .release:
                return [
                    "SWIFT_OPTIMIZATION_LEVEL": "-O",
                    "GCC_OPTIMIZATION_LEVEL": "s",
                    "DEBUG_INFORMATION_FORMAT": "dwarf-with-dsym",
                    "ENABLE_TESTABILITY": "NO"
                ]
            case .profile:
                return [
                    "SWIFT_OPTIMIZATION_LEVEL": "-O",
                    "GCC_OPTIMIZATION_LEVEL": "s",
                    "DEBUG_INFORMATION_FORMAT": "dwarf-with-dsym",
                    "ENABLE_TESTABILITY": "YES"
                ]
            case .staging:
                return [
                    "SWIFT_OPTIMIZATION_LEVEL": "-Osize",
                    "GCC_OPTIMIZATION_LEVEL": "s",
                    "DEBUG_INFORMATION_FORMAT": "dwarf",
                    "ENABLE_TESTABILITY": "YES"
                ]
            }
        }
    }
    
    /// Initialize the build configuration service
    public init() {}
    
    /// Generate build settings string for xcodebuild
    /// - Parameter configuration: The configuration to use
    /// - Returns: A string of build settings flags
    public func generateBuildSettings(for configuration: Configuration) -> String {
        configuration.buildSettings.map { "\($0.key)=\($0.value)" }.joined(separator: " ")
    }
    
    /// Get all available configurations
    /// - Returns: Array of configuration names
    public func availableConfigurations() -> [String] {
        Configuration.allCases.map { $0.rawValue }
    }
}
