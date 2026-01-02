import Foundation

/// Service for analyzing and optimizing build processes
public class BuildOptimizationService {
    
    /// Build optimization suggestions
    public struct OptimizationSuggestion {
        public let category: Category
        public let title: String
        public let description: String
        public let impact: Impact
        public let recommendation: String
        
        public init(category: Category, title: String, description: String, impact: Impact, recommendation: String) {
            self.category = category
            self.title = title
            self.description = description
            self.impact = impact
            self.recommendation = recommendation
        }
    }
    
    /// Optimization categories
    public enum Category: String {
        case compilation = "Compilation"
        case linking = "Linking"
        case codeSignin = "Code Signing"
        case dependencies = "Dependencies"
        case caching = "Caching"
        case parallelization = "Parallelization"
    }
    
    /// Impact level
    public enum Impact: String {
        case high = "High"
        case medium = "Medium"
        case low = "Low"
    }
    
    /// Build metrics
    public struct BuildMetrics {
        public let totalTime: TimeInterval
        public let compilationTime: TimeInterval
        public let linkingTime: TimeInterval
        public let codeSigningTime: TimeInterval
        public let parallelizationEfficiency: Double
        
        public init(
            totalTime: TimeInterval,
            compilationTime: TimeInterval,
            linkingTime: TimeInterval,
            codeSigningTime: TimeInterval,
            parallelizationEfficiency: Double
        ) {
            self.totalTime = totalTime
            self.compilationTime = compilationTime
            self.linkingTime = linkingTime
            self.codeSigningTime = codeSigningTime
            self.parallelizationEfficiency = parallelizationEfficiency
        }
    }
    
    /// Initialize the build optimization service
    public init() {}
    
    /// Analyze build and provide optimization suggestions
    /// - Parameter metrics: Build metrics to analyze
    /// - Returns: Array of optimization suggestions
    public func analyzeBuild(metrics: BuildMetrics) -> [OptimizationSuggestion] {
        var suggestions: [OptimizationSuggestion] = []
        
        // Check compilation time
        if metrics.compilationTime > metrics.totalTime * 0.5 {
            suggestions.append(OptimizationSuggestion(
                category: .compilation,
                title: "Enable Whole Module Optimization",
                description: "Compilation takes \(Int(metrics.compilationTime))s, which is more than 50% of total build time",
                impact: .high,
                recommendation: "Add SWIFT_WHOLE_MODULE_OPTIMIZATION=YES for release builds"
            ))
        }
        
        // Check parallelization
        if metrics.parallelizationEfficiency < 0.6 {
            suggestions.append(OptimizationSuggestion(
                category: .parallelization,
                title: "Improve Build Parallelization",
                description: "Parallelization efficiency is \(Int(metrics.parallelizationEfficiency * 100))%",
                impact: .high,
                recommendation: "Review module dependencies and enable parallel builds with -jobs flag"
            ))
        }
        
        // Check code signing time
        if metrics.codeSigningTime > 30 {
            suggestions.append(OptimizationSuggestion(
                category: .codeSignin,
                title: "Optimize Code Signing",
                description: "Code signing takes \(Int(metrics.codeSigningTime))s",
                impact: .medium,
                recommendation: "Disable code signing for development builds with CODE_SIGN_IDENTITY=''"
            ))
        }
        
        return suggestions
    }
    
    /// Generate optimized build settings
    /// - Parameter buildType: Type of build (debug/release)
    /// - Returns: Dictionary of optimized build settings
    public func generateOptimizedSettings(buildType: String) -> [String: String] {
        var settings: [String: String] = [:]
        
        if buildType.lowercased() == "debug" {
            settings = [
                "DEBUG_INFORMATION_FORMAT": "dwarf",
                "COMPILER_INDEX_STORE_ENABLE": "NO",
                "CODE_SIGN_IDENTITY": "",
                "CODE_SIGNING_REQUIRED": "NO",
                "SWIFT_COMPILATION_MODE": "incremental"
            ]
        } else {
            settings = [
                "SWIFT_WHOLE_MODULE_OPTIMIZATION": "YES",
                "SWIFT_OPTIMIZATION_LEVEL": "-O",
                "SWIFT_COMPILATION_MODE": "wholemodule",
                "DEAD_CODE_STRIPPING": "YES",
                "STRIP_INSTALLED_PRODUCT": "YES"
            ]
        }
        
        return settings
    }
    
    /// Generate build command with optimizations
    /// - Parameters:
    ///   - baseCommand: Base build command
    ///   - buildType: Build type
    /// - Returns: Optimized build command
    public func generateOptimizedCommand(baseCommand: String, buildType: String) -> String {
        let settings = generateOptimizedSettings(buildType: buildType)
        let settingsString = settings.map { "\($0.key)=\($0.value)" }.joined(separator: " ")
        return "\(baseCommand) \(settingsString)"
    }
}
