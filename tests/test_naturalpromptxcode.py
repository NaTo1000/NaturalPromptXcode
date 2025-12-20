"""Unit tests for NaturalPromptXcode."""

import pytest
from src.config import Config
from src.nlp.parser import PromptParser, AppRequirements
from src.codegen.generator import CodeGenerator, ProjectStructure


class TestConfig:
    """Tests for configuration management."""
    
    def test_config_defaults(self):
        """Test default configuration values."""
        config = Config()
        assert config.model_name == "gpt-4"
        assert config.ui_framework == "swiftui"
        assert config.language == "swift"
        assert config.target_ios_version == "15.0"
    
    def test_config_verbose_flag(self):
        """Test verbose flag."""
        config = Config()
        assert config.verbose is False
        config.verbose = True
        assert config.verbose is True


class TestPromptParser:
    """Tests for prompt parsing."""
    
    def test_parse_counter_app(self):
        """Test parsing counter app prompt."""
        config = Config()
        parser = PromptParser(config)
        
        prompt = "Create a simple counter app with increment and decrement buttons"
        requirements = parser.parse(prompt)
        
        assert isinstance(requirements, AppRequirements)
        assert requirements.app_name == "CounterApp"
        assert len(requirements.features) > 0
        assert requirements.features[0].name == "Counter"
    
    def test_parse_weather_app(self):
        """Test parsing weather app prompt."""
        config = Config()
        parser = PromptParser(config)
        
        prompt = "Create a weather app that shows temperature"
        requirements = parser.parse(prompt)
        
        assert requirements.app_name == "WeatherApp"
        assert len(requirements.features) > 0
    
    def test_parse_generic_app(self):
        """Test parsing generic app prompt."""
        config = Config()
        parser = PromptParser(config)
        
        prompt = "Create an awesome app"
        requirements = parser.parse(prompt)
        
        assert requirements.app_name == "GeneratedApp"
        assert len(requirements.features) > 0


class TestCodeGenerator:
    """Tests for code generation."""
    
    def test_generate_swiftui_project(self):
        """Test generating SwiftUI project."""
        config = Config()
        config.ui_framework = "swiftui"
        
        parser = PromptParser(config)
        requirements = parser.parse("Create a counter app")
        
        generator = CodeGenerator(config)
        project = generator.generate(requirements)
        
        assert isinstance(project, ProjectStructure)
        assert project.name == "CounterApp"
        assert len(project.files) > 0
        
        # Check for expected files
        file_paths = [f.path for f in project.files]
        assert any("App.swift" in path for path in file_paths)
        assert "ContentView.swift" in file_paths
        assert "Info.plist" in file_paths
    
    def test_generate_uikit_project(self):
        """Test generating UIKit project."""
        config = Config()
        config.ui_framework = "uikit"
        
        parser = PromptParser(config)
        requirements = parser.parse("Create a counter app")
        requirements.ui_framework = "uikit"
        
        generator = CodeGenerator(config)
        project = generator.generate(requirements)
        
        assert isinstance(project, ProjectStructure)
        file_paths = [f.path for f in project.files]
        assert "AppDelegate.swift" in file_paths
        assert "ViewController.swift" in file_paths
    
    def test_generated_code_contains_swift(self):
        """Test that generated files contain Swift code."""
        config = Config()
        parser = PromptParser(config)
        requirements = parser.parse("Create a counter app")
        
        generator = CodeGenerator(config)
        project = generator.generate(requirements)
        
        # Find ContentView.swift
        content_view = next(
            (f for f in project.files if f.path == "ContentView.swift"),
            None
        )
        
        assert content_view is not None
        assert "import SwiftUI" in content_view.content
        assert "struct ContentView" in content_view.content
        assert "var body: some View" in content_view.content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
