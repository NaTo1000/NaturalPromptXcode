"""Unit tests for NaturalPromptXcode."""

import pytest
import tempfile
from pathlib import Path
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

    def test_config_validation_invalid_framework(self):
        """Test configuration validation for invalid framework."""
        config = Config()
        config.ui_framework = "invalid"
        with pytest.raises(ValueError):
            config._validate_config()

    def test_config_validation_invalid_temperature(self):
        """Test configuration validation for invalid temperature."""
        config = Config()
        config.temperature = 2.0
        with pytest.raises(ValueError):
            config._validate_config()

    def test_config_optimization_defaults(self):
        """Test optimization-related configuration defaults."""
        config = Config()
        assert config.enable_caching is True
        assert config.batch_file_operations is True
        assert hasattr(config, "cache_dir")


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

    def test_parse_caching(self):
        """Test that parsing uses caching for repeated prompts."""
        config = Config()
        config.enable_caching = True

        # Use a temporary cache directory
        with tempfile.TemporaryDirectory() as tmpdir:
            config.cache_dir = tmpdir
            parser = PromptParser(config)

            prompt = "Create a counter app"

            # First parse
            result1 = parser.parse(prompt)

            # Second parse should use cache
            result2 = parser.parse(prompt)

            # Both should have same structure
            assert result1.app_name == result2.app_name
            assert len(result1.features) == len(result2.features)

    def test_parse_cache_key_generation(self):
        """Test that cache keys are generated correctly."""
        config = Config()
        parser = PromptParser(config)

        key1 = parser._get_cache_key("test prompt")
        key2 = parser._get_cache_key("test prompt")
        key3 = parser._get_cache_key("different prompt")

        # Same prompt should generate same key
        assert key1 == key2
        # Different prompt should generate different key
        assert key1 != key3


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
            (f for f in project.files if f.path == "ContentView.swift"), None
        )

        assert content_view is not None
        assert "import SwiftUI" in content_view.content
        assert "struct ContentView" in content_view.content
        assert "var body: some View" in content_view.content

    def test_generator_file_generation_dispatch(self):
        """Test the file generation dispatch mechanism."""
        config = Config()
        parser = PromptParser(config)
        requirements = parser.parse("Create a counter app")

        generator = CodeGenerator(config)

        # Test individual file generation
        app_file = generator._generate_file("swiftui_app", requirements)
        assert app_file is not None
        assert app_file.file_type == "swift"

        content_file = generator._generate_file("swiftui_content_view", requirements)
        assert content_file is not None
        assert "ContentView" in content_file.content


class TestPerformanceOptimizations:
    """Tests for performance optimization features."""

    def test_batch_file_operations(self):
        """Test batch file writing optimization."""
        from src.builder.xcode import XcodeProjectBuilder

        config = Config()
        config.batch_file_operations = True

        builder = XcodeProjectBuilder(config)

        # Create a simple project structure for testing
        from src.codegen.generator import ProjectFile

        files = [
            ProjectFile("test1.swift", "content1", "swift"),
            ProjectFile("test2.swift", "content2", "swift"),
            ProjectFile("subdir/test3.swift", "content3", "swift"),
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            test_path = Path(tmpdir) / "test_src"
            test_path.mkdir()

            # This should work without errors
            builder._batch_write_files(files, test_path)

            # Verify files were created
            assert (test_path / "test1.swift").exists()
            assert (test_path / "test2.swift").exists()
            assert (test_path / "subdir/test3.swift").exists()

    def test_config_early_validation(self):
        """Test that configuration validates early to fail fast."""
        config = Config()

        # Valid configuration should not raise
        config._validate_config()

        # Invalid framework should raise immediately
        config.ui_framework = "invalid_framework"
        with pytest.raises(ValueError) as exc_info:
            config._validate_config()
        assert "framework" in str(exc_info.value).lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
