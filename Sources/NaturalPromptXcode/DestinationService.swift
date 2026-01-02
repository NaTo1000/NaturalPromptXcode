import Foundation

/// Service for managing build destinations and platforms
public class DestinationService {
    
    /// Represents a build destination
    public struct Destination {
        public let platform: Platform
        public let device: String
        public let osVersion: String?
        
        public init(platform: Platform, device: String, osVersion: String? = nil) {
            self.platform = platform
            self.device = device
            self.osVersion = osVersion
        }
        
        public var destinationString: String {
            var components = ["platform=\(platform.rawValue)", "name=\(device)"]
            if let os = osVersion {
                components.append("OS=\(os)")
            }
            return components.joined(separator: ",")
        }
    }
    
    /// Supported platforms
    public enum Platform: String, CaseIterable {
        case iOS = "iOS"
        case iOSSimulator = "iOS Simulator"
        case macOS = "macOS"
        case tvOS = "tvOS"
        case tvOSSimulator = "tvOS Simulator"
        case watchOS = "watchOS"
        case watchOSSimulator = "watchOS Simulator"
        case visionOS = "visionOS"
        case visionOSSimulator = "visionOS Simulator"
        
        public var defaultDevices: [String] {
            switch self {
            case .iOS, .iOSSimulator:
                return ["iPhone 14", "iPhone 14 Pro", "iPhone 15", "iPad Pro (12.9-inch)"]
            case .macOS:
                return ["My Mac", "Any Mac"]
            case .tvOS, .tvOSSimulator:
                return ["Apple TV", "Apple TV 4K"]
            case .watchOS, .watchOSSimulator:
                return ["Apple Watch Series 9 (45mm)", "Apple Watch Ultra"]
            case .visionOS, .visionOSSimulator:
                return ["Apple Vision Pro"]
            }
        }
    }
    
    /// Initialize the destination service
    public init() {}
    
    /// Get common destinations for a platform
    /// - Parameter platform: The platform to get destinations for
    /// - Returns: Array of common destinations
    public func commonDestinations(for platform: Platform) -> [Destination] {
        platform.defaultDevices.map { device in
            Destination(platform: platform, device: device)
        }
    }
    
    /// Get all simulator destinations
    /// - Returns: Array of all simulator destinations
    public func allSimulatorDestinations() -> [Destination] {
        let simulatorPlatforms: [Platform] = [.iOSSimulator, .tvOSSimulator, .watchOSSimulator, .visionOSSimulator]
        return simulatorPlatforms.flatMap { commonDestinations(for: $0) }
    }
    
    /// Parse destination string from natural language
    /// - Parameter prompt: Natural language description
    /// - Returns: Destination if parseable
    public func parseDestination(from prompt: String) -> Destination? {
        let lowercased = prompt.lowercased()
        
        // Check for platform keywords
        if lowercased.contains("iphone") || lowercased.contains("ios") {
            let device = lowercased.contains("14 pro") ? "iPhone 14 Pro" : "iPhone 14"
            return Destination(platform: .iOSSimulator, device: device)
        } else if lowercased.contains("ipad") {
            return Destination(platform: .iOSSimulator, device: "iPad Pro (12.9-inch)")
        } else if lowercased.contains("mac") {
            return Destination(platform: .macOS, device: "My Mac")
        } else if lowercased.contains("watch") {
            return Destination(platform: .watchOSSimulator, device: "Apple Watch Series 9 (45mm)")
        } else if lowercased.contains("tv") {
            return Destination(platform: .tvOSSimulator, device: "Apple TV 4K")
        } else if lowercased.contains("vision") {
            return Destination(platform: .visionOSSimulator, device: "Apple Vision Pro")
        }
        
        return nil
    }
}
