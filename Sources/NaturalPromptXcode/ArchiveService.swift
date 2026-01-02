import Foundation

/// Service for managing build archives and exports
public class ArchiveService {
    
    /// Export method for archives
    public enum ExportMethod: String, CaseIterable {
        case appStore = "app-store"
        case adHoc = "ad-hoc"
        case development = "development"
        case enterprise = "enterprise"
        case validation = "validation"
        
        public var description: String {
            switch self {
            case .appStore:
                return "App Store distribution"
            case .adHoc:
                return "Ad-Hoc distribution"
            case .development:
                return "Development distribution"
            case .enterprise:
                return "Enterprise distribution"
            case .validation:
                return "Validation only"
            }
        }
    }
    
    /// Export options
    public struct ExportOptions {
        public let method: ExportMethod
        public let teamID: String?
        public let provisioningProfiles: [String: String]
        public let compileBitcode: Bool
        public let uploadSymbols: Bool
        
        public init(
            method: ExportMethod,
            teamID: String?,
            provisioningProfiles: [String: String],
            compileBitcode: Bool = true,
            uploadSymbols: Bool = true
        ) {
            self.method = method
            self.teamID = teamID
            self.provisioningProfiles = provisioningProfiles
            self.compileBitcode = compileBitcode
            self.uploadSymbols = uploadSymbols
        }
    }
    
    /// Initialize the archive service
    public init() {}
    
    /// Generate archive command
    /// - Parameters:
    ///   - project: Project or workspace path
    ///   - scheme: Scheme to archive
    ///   - archivePath: Output archive path
    ///   - configuration: Build configuration
    /// - Returns: Complete xcodebuild archive command
    public func generateArchiveCommand(
        project: String,
        scheme: String,
        archivePath: String,
        configuration: String = "Release"
    ) -> String {
        let projectFlag = project.hasSuffix(".xcworkspace") ? "-workspace" : "-project"
        return """
        xcodebuild archive \
            \(projectFlag) \(project) \
            -scheme \(scheme) \
            -configuration \(configuration) \
            -archivePath \(archivePath) \
            -destination "generic/platform=iOS"
        """
    }
    
    /// Generate export command
    /// - Parameters:
    ///   - archivePath: Path to archive
    ///   - exportPath: Output export path
    ///   - options: Export options
    /// - Returns: Complete xcodebuild export command
    public func generateExportCommand(
        archivePath: String,
        exportPath: String,
        options: ExportOptions
    ) -> String {
        return """
        xcodebuild -exportArchive \
            -archivePath \(archivePath) \
            -exportPath \(exportPath) \
            -exportOptionsPlist exportOptions.plist
        """
    }
    
    /// Generate export options plist content
    /// - Parameter options: Export options
    /// - Returns: Plist XML string
    public func generateExportOptionsPlist(options: ExportOptions) -> String {
        var plist = """
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
        <plist version="1.0">
        <dict>
            <key>method</key>
            <string>\(options.method.rawValue)</string>
        """
        
        if let teamID = options.teamID {
            plist += """
            
                <key>teamID</key>
                <string>\(teamID)</string>
            """
        }
        
        plist += """
        
            <key>compileBitcode</key>
            <\(options.compileBitcode ? "true" : "false")/>
            <key>uploadSymbols</key>
            <\(options.uploadSymbols ? "true" : "false")/>
        </dict>
        </plist>
        """
        
        return plist
    }
    
    /// Generate complete archive and export workflow
    /// - Parameters:
    ///   - project: Project path
    ///   - scheme: Scheme name
    ///   - outputDir: Output directory
    ///   - options: Export options
    /// - Returns: Array of commands to execute
    public func generateCompleteWorkflow(
        project: String,
        scheme: String,
        outputDir: String,
        options: ExportOptions
    ) -> [String] {
        let archivePath = "\(outputDir)/\(scheme).xcarchive"
        let exportPath = "\(outputDir)/export"
        
        return [
            "mkdir -p \(outputDir)",
            generateArchiveCommand(project: project, scheme: scheme, archivePath: archivePath),
            generateExportCommand(archivePath: archivePath, exportPath: exportPath, options: options)
        ]
    }
}
