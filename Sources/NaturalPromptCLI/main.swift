import Foundation
import NaturalPromptXcode

@main
struct NaturalPromptCLI {
    static func main() {
        print("🚀 NaturalPromptXcode v\(NaturalPromptXcode.version)")
        print("Natural language prompt to Xcode build commands")
        print()
        
        let arguments = CommandLine.arguments
        
        if arguments.count < 2 {
            printUsage()
            return
        }
        
        let command = arguments[1]
        
        switch command {
        case "process":
            if arguments.count < 3 {
                print("Error: Missing prompt argument")
                printUsage()
                return
            }
            let prompt = arguments[2...].joined(separator: " ")
            processPrompt(prompt)
            
        case "detect":
            detectProjects()
            
        case "version":
            print("Version: \(NaturalPromptXcode.version)")
            
        case "help", "--help", "-h":
            printUsage()
            
        default:
            print("Unknown command: \(command)")
            printUsage()
        }
    }
    
    static func processPrompt(_ prompt: String) {
        print("Processing prompt: \"\(prompt)\"")
        print()
        
        let processor = NaturalPromptXcode()
        let commands = processor.processPrompt(prompt)
        
        if commands.isEmpty {
            print("No commands generated from prompt")
            return
        }
        
        print("Generated commands:")
        for (index, command) in commands.enumerated() {
            print("\(index + 1). \(command)")
        }
    }
    
    static func detectProjects() {
        print("Detecting Xcode projects...")
        print()
        
        let processor = NaturalPromptXcode()
        let projects = processor.detectProjects()
        
        if projects.isEmpty {
            print("No Xcode projects found in current directory")
            return
        }
        
        print("Found \(projects.count) project(s):")
        for project in projects {
            print("  - \(project)")
        }
    }
    
    static func printUsage() {
        print("""
        Usage: natural-prompt <command> [arguments]
        
        Commands:
          process <prompt>    Process a natural language prompt and generate Xcode commands
          detect              Detect Xcode projects in the current directory
          version             Show version information
          help                Show this help message
        
        Examples:
          natural-prompt process "build the iOS app"
          natural-prompt process "run tests for the project"
          natural-prompt process "clean and build everything"
          natural-prompt detect
        
        For more information, visit: https://github.com/NaTo1000/NaturalPromptXcode
        """)
    }
}
