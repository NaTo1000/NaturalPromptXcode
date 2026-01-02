import Foundation

/// Service for managing code signing and provisioning
public class CodeSigningService {
    
    /// Code signing identity
    public struct SigningIdentity {
        public let name: String
        public let teamID: String?
        public let type: IdentityType
        
        public init(name: String, teamID: String?, type: IdentityType) {
            self.name = name
            self.teamID = teamID
            self.type = type
        }
    }
    
    /// Identity types
    public enum IdentityType: String {
        case development = "Apple Development"
        case distribution = "Apple Distribution"
        case developerID = "Developer ID Application"
        case none = "Sign to Run Locally"
    }
    
    /// Provisioning profile
    public struct ProvisioningProfile {
        public let name: String
        public let uuid: String
        public let appID: String
        public let expirationDate: Date?
        
        public init(name: String, uuid: String, appID: String, expirationDate: Date?) {
            self.name = name
            self.uuid = uuid
            self.appID = appID
            self.expirationDate = expirationDate
        }
    }
    
    /// Initialize the code signing service
    public init() {}
    
    /// Generate code signing build settings
    /// - Parameters:
    ///   - identity: Signing identity to use
    ///   - profile: Provisioning profile to use
    /// - Returns: Dictionary of build settings
    public func generateSigningSettings(
        identity: SigningIdentity,
        profile: ProvisioningProfile?
    ) -> [String: String] {
        var settings: [String: String] = [
            "CODE_SIGN_IDENTITY": identity.name
        ]
        
        if let teamID = identity.teamID {
            settings["DEVELOPMENT_TEAM"] = teamID
        }
        
        if let profile = profile {
            settings["PROVISIONING_PROFILE_SPECIFIER"] = profile.name
            settings["PROVISIONING_PROFILE"] = profile.uuid
        }
        
        return settings
    }
    
    /// Generate command for automatic signing
    /// - Parameter teamID: Development team ID
    /// - Returns: Build settings string
    public func generateAutomaticSigningSettings(teamID: String) -> String {
        let settings = [
            "CODE_SIGN_STYLE=Automatic",
            "DEVELOPMENT_TEAM=\(teamID)",
            "CODE_SIGN_IDENTITY=Apple Development"
        ]
        return settings.joined(separator: " ")
    }
    
    /// Generate command for manual signing
    /// - Parameters:
    ///   - identity: Signing identity
    ///   - profile: Provisioning profile UUID
    /// - Returns: Build settings string
    public func generateManualSigningSettings(
        identity: String,
        profile: String
    ) -> String {
        let settings = [
            "CODE_SIGN_STYLE=Manual",
            "CODE_SIGN_IDENTITY=\(identity)",
            "PROVISIONING_PROFILE=\(profile)"
        ]
        return settings.joined(separator: " ")
    }
}
