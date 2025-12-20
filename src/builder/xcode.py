"""Xcode project builder module."""

import os
import subprocess
from pathlib import Path
from typing import Optional

try:
    from ..codegen.generator import ProjectStructure
except ImportError:
    from codegen.generator import ProjectStructure


class XcodeProjectBuilder:
    """Build and manage Xcode projects."""
    
    def __init__(self, config):
        """
        Initialize the project builder.
        
        Args:
            config: Configuration object
        """
        self.config = config
    
    def create_project(self, project: ProjectStructure, output_dir: str) -> str:
        """
        Create Xcode project structure on disk.
        
        Args:
            project: Project structure to create
            output_dir: Directory to create project in
            
        Returns:
            Path to created project directory
        """
        # Create project directory
        project_path = Path(output_dir) / project.name
        project_path.mkdir(parents=True, exist_ok=True)
        
        if self.config.verbose:
            print(f"      Creating project at: {project_path}")
        
        # Create source directory
        src_path = project_path / project.name
        src_path.mkdir(exist_ok=True)
        
        # Write all files
        for file in project.files:
            file_path = src_path / file.path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w') as f:
                f.write(file.content)
            
            if self.config.verbose:
                print(f"      Created: {file.path}")
        
        # Create a basic project.pbxproj file
        self._create_pbxproj(project, project_path)
        
        return str(project_path)
    
    def _create_pbxproj(self, project: ProjectStructure, project_path: Path):
        """Create Xcode project.pbxproj file."""
        xcodeproj_path = project_path / f"{project.name}.xcodeproj"
        xcodeproj_path.mkdir(exist_ok=True)
        
        # This is a simplified pbxproj - in production, use a proper library
        # like xcodeproj or generate via xcodebuild
        pbxproj_content = f"""// !$*UTF8*$!
{{
    archiveVersion = 1;
    classes = {{
    }};
    objectVersion = 55;
    objects = {{
    }};
    rootObject = /* Project object */;
}}
"""
        pbxproj_path_file = xcodeproj_path / "project.pbxproj"
        with open(pbxproj_path_file, 'w') as f:
            f.write(pbxproj_content)
        
        if self.config.verbose:
            print(f"      Created: {project.name}.xcodeproj")
    
    def build(self, project_path: str, configuration: str = "Debug") -> str:
        """
        Build the Xcode project.
        
        Args:
            project_path: Path to project directory
            configuration: Build configuration (Debug or Release)
            
        Returns:
            Path to built application
        """
        project_path = Path(project_path)
        project_name = project_path.name
        
        # Find .xcodeproj
        xcodeproj = project_path / f"{project_name}.xcodeproj"
        
        if not xcodeproj.exists():
            raise FileNotFoundError(f"Xcode project not found: {xcodeproj}")
        
        # Build command
        build_dir = project_path / "build"
        build_dir.mkdir(exist_ok=True)
        
        cmd = [
            "xcodebuild",
            "-project", str(xcodeproj),
            "-scheme", project_name,
            "-configuration", configuration,
            "-derivedDataPath", str(build_dir),
            "build"
        ]
        
        if self.config.verbose:
            print(f"      Running: {' '.join(cmd)}")
        
        # Run build (note: this is a placeholder)
        # In reality, we'd need proper scheme setup
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode != 0:
                if self.config.verbose:
                    print(f"      Build output: {result.stdout}")
                    print(f"      Build errors: {result.stderr}")
                raise RuntimeError(f"Build failed with code {result.returncode}")
            
            # Find built app
            app_path = build_dir / "Build" / "Products" / configuration / f"{project_name}.app"
            return str(app_path)
            
        except subprocess.TimeoutExpired:
            raise RuntimeError("Build timed out after 5 minutes")
        except FileNotFoundError:
            raise RuntimeError("xcodebuild not found. Please install Xcode Command Line Tools.")
