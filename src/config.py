"""Configuration management for NaturalPromptXcode."""

import os
from pathlib import Path
from typing import Optional
import yaml


class Config:
    """Configuration container for NaturalPromptXcode."""

    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration.

        Args:
            config_file: Path to YAML configuration file
        """
        # Default values
        self.model_name = "gpt-4"
        self.model_provider = "openai"
        self.temperature = 0.7
        self.max_tokens = 2000

        self.ui_framework = "swiftui"
        self.language = "swift"
        self.target_ios_version = "15.0"

        self.output_dir = "./output"
        self.clean_before_build = True
        self.verbose = False

        # Performance optimization settings
        self.enable_caching = True
        self.cache_dir = "./.cache/npx"
        self.batch_file_operations = True

        # Load from file if provided
        if config_file and Path(config_file).exists():
            self._load_from_file(config_file)

        # Override with environment variables
        self._load_from_env()

        # Validate configuration
        self._validate_config()

    def _load_from_file(self, config_file: str):
        """Load configuration from YAML file."""
        with open(config_file, "r") as f:
            data = yaml.safe_load(f)

        if "model" in data:
            self.model_name = data["model"].get("name", self.model_name)
            self.model_provider = data["model"].get("provider", self.model_provider)
            self.temperature = data["model"].get("temperature", self.temperature)
            self.max_tokens = data["model"].get("max_tokens", self.max_tokens)

        if "build" in data:
            self.ui_framework = data["build"].get(
                "default_framework", self.ui_framework
            )
            self.language = data["build"].get("default_language", self.language)
            self.target_ios_version = data["build"].get(
                "target_ios_version", self.target_ios_version
            )

        if "output" in data:
            self.output_dir = data["output"].get("default_dir", self.output_dir)
            self.clean_before_build = data["output"].get(
                "clean_before_build", self.clean_before_build
            )

    def _load_from_env(self):
        """Load configuration from environment variables."""
        if "OPENAI_API_KEY" in os.environ:
            self.api_key = os.environ["OPENAI_API_KEY"]

        if "NPX_MODEL" in os.environ:
            self.model_name = os.environ["NPX_MODEL"]

        if "NPX_OUTPUT_DIR" in os.environ:
            self.output_dir = os.environ["NPX_OUTPUT_DIR"]

    def _validate_config(self):
        """Validate configuration for early error detection."""
        # Validate UI framework
        valid_frameworks = ["swiftui", "uikit"]
        if self.ui_framework not in valid_frameworks:
            raise ValueError(
                f"Invalid UI framework: {self.ui_framework}. Must be one of {valid_frameworks}"
            )

        # Validate language
        valid_languages = ["swift", "objective-c"]
        if self.language not in valid_languages:
            raise ValueError(
                f"Invalid language: {self.language}. Must be one of {valid_languages}"
            )

        # Validate temperature
        if not 0.0 <= self.temperature <= 1.0:
            raise ValueError(
                f"Invalid temperature: {self.temperature}. Must be between 0.0 and 1.0"
            )

        # Validate max_tokens
        if self.max_tokens <= 0:
            raise ValueError(f"Invalid max_tokens: {self.max_tokens}. Must be positive")
