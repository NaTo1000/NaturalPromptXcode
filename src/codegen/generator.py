"""Code generation module."""

from typing import List, Dict, Any
from dataclasses import dataclass, field

from ..nlp.parser import AppRequirements


@dataclass
class ProjectFile:
    """Represents a file in the generated project."""
    path: str
    content: str
    file_type: str  # "swift", "plist", "storyboard", etc.


@dataclass
class ProjectStructure:
    """Complete project structure with all files."""
    name: str
    files: List[ProjectFile] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class CodeGenerator:
    """Generate iOS code from structured requirements."""
    
    def __init__(self, config):
        """
        Initialize the code generator.
        
        Args:
            config: Configuration object
        """
        self.config = config
    
    def generate(self, requirements: AppRequirements) -> ProjectStructure:
        """
        Generate complete project structure from requirements.
        
        Args:
            requirements: Parsed app requirements
            
        Returns:
            ProjectStructure with all generated files
        """
        project = ProjectStructure(
            name=requirements.app_name,
            metadata={
                "framework": requirements.ui_framework,
                "language": self.config.language,
                "ios_version": self.config.target_ios_version
            }
        )
        
        # Generate main app file
        if requirements.ui_framework == "swiftui":
            project.files.append(self._generate_swiftui_app(requirements))
            project.files.append(self._generate_swiftui_content_view(requirements))
        else:
            project.files.append(self._generate_uikit_app_delegate(requirements))
            project.files.append(self._generate_uikit_view_controller(requirements))
        
        # Generate Info.plist
        project.files.append(self._generate_info_plist(requirements))
        
        return project
    
    def _generate_swiftui_app(self, requirements: AppRequirements) -> ProjectFile:
        """Generate SwiftUI App file."""
        content = f"""import SwiftUI

@main
struct {requirements.app_name}: App {{
    var body: some Scene {{
        WindowGroup {{
            ContentView()
        }}
    }}
}}
"""
        return ProjectFile(
            path=f"{requirements.app_name}App.swift",
            content=content,
            file_type="swift"
        )
    
    def _generate_swiftui_content_view(self, requirements: AppRequirements) -> ProjectFile:
        """Generate SwiftUI ContentView."""
        # Generate based on features
        view_code = self._generate_view_code(requirements)
        
        content = f"""import SwiftUI

struct ContentView: View {{
{view_code}
}}

struct ContentView_Previews: PreviewProvider {{
    static var previews: some View {{
        ContentView()
    }}
}}
"""
        return ProjectFile(
            path="ContentView.swift",
            content=content,
            file_type="swift"
        )
    
    def _generate_view_code(self, requirements: AppRequirements) -> str:
        """Generate view code based on features."""
        if not requirements.features:
            return """    var body: some View {
        Text("Hello, World!")
            .padding()
    }"""
        
        feature = requirements.features[0]
        
        if feature.name == "Counter":
            return """    @State private var count = 0
    
    var body: some View {
        VStack(spacing: 20) {
            Text("Counter: \\(count)")
                .font(.largeTitle)
                .fontWeight(.bold)
            
            HStack(spacing: 20) {
                Button(action: {
                    count -= 1
                }) {
                    Image(systemName: "minus.circle.fill")
                        .font(.system(size: 50))
                }
                
                Button(action: {
                    count += 1
                }) {
                    Image(systemName: "plus.circle.fill")
                        .font(.system(size: 50))
                }
            }
        }
        .padding()
    }"""
        
        elif feature.name == "WeatherDisplay":
            return """    @State private var temperature = "72°F"
    @State private var condition = "Sunny"
    
    var body: some View {
        VStack(spacing: 20) {
            Image(systemName: "sun.max.fill")
                .font(.system(size: 100))
                .foregroundColor(.orange)
            
            Text(temperature)
                .font(.system(size: 60))
                .fontWeight(.bold)
            
            Text(condition)
                .font(.title)
                .foregroundColor(.secondary)
        }
        .padding()
    }"""
        
        else:
            return f"""    var body: some View {{
        VStack {{
            Text("Welcome to {requirements.app_name}")
                .font(.largeTitle)
                .padding()
        }}
    }}"""
    
    def _generate_uikit_app_delegate(self, requirements: AppRequirements) -> ProjectFile:
        """Generate UIKit AppDelegate."""
        content = f"""import UIKit

@main
class AppDelegate: UIResponder, UIApplicationDelegate {{

    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {{
        return true
    }}

    func application(_ application: UIApplication, configurationForConnecting connectingSceneSession: UISceneSession, options: UIScene.ConnectionOptions) -> UISceneConfiguration {{
        return UISceneConfiguration(name: "Default Configuration", sessionRole: connectingSceneSession.role)
    }}
}}
"""
        return ProjectFile(
            path="AppDelegate.swift",
            content=content,
            file_type="swift"
        )
    
    def _generate_uikit_view_controller(self, requirements: AppRequirements) -> ProjectFile:
        """Generate UIKit ViewController."""
        content = f"""import UIKit

class ViewController: UIViewController {{

    override func viewDidLoad() {{
        super.viewDidLoad()
        view.backgroundColor = .systemBackground
        
        let label = UILabel()
        label.text = "Hello from {requirements.app_name}!"
        label.textAlignment = .center
        label.translatesAutoresizingMaskIntoConstraints = false
        
        view.addSubview(label)
        
        NSLayoutConstraint.activate([
            label.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            label.centerYAnchor.constraint(equalTo: view.centerYAnchor)
        ])
    }}
}}
"""
        return ProjectFile(
            path="ViewController.swift",
            content=content,
            file_type="swift"
        )
    
    def _generate_info_plist(self, requirements: AppRequirements) -> ProjectFile:
        """Generate Info.plist file."""
        content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>en</string>
    <key>CFBundleDisplayName</key>
    <string>{requirements.app_name}</string>
    <key>CFBundleExecutable</key>
    <string>$(EXECUTABLE_NAME)</string>
    <key>CFBundleIdentifier</key>
    <string>$(PRODUCT_BUNDLE_IDENTIFIER)</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>$(PRODUCT_NAME)</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleVersion</key>
    <string>1</string>
    <key>LSRequiresIPhoneOS</key>
    <true/>
    <key>UILaunchStoryboardName</key>
    <string>LaunchScreen</string>
    <key>UIRequiredDeviceCapabilities</key>
    <array>
        <string>armv7</string>
    </array>
    <key>UISupportedInterfaceOrientations</key>
    <array>
        <string>UIInterfaceOrientationPortrait</string>
    </array>
</dict>
</plist>
"""
        return ProjectFile(
            path="Info.plist",
            content=content,
            file_type="plist"
        )
