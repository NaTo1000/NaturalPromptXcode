"""Natural Language Processing module for prompt parsing."""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path


@dataclass
class AppFeature:
    """Represents a single app feature."""

    name: str
    description: str
    ui_elements: List[str]
    functionality: List[str]


@dataclass
class AppRequirements:
    """Parsed requirements from natural language prompt."""

    app_name: str
    description: str
    features: List[AppFeature]
    ui_framework: str
    metadata: Dict[str, Any]


class PromptParser:
    """Parse natural language prompts into structured requirements."""

    def __init__(self, config):
        """
        Initialize the parser.

        Args:
            config: Configuration object
        """
        self.config = config
        self._cache = {}  # In-memory cache for parsed prompts
        self._cache_dir = None

        # Set up disk cache if enabled
        if hasattr(config, "enable_caching") and config.enable_caching:
            self._cache_dir = Path(config.cache_dir) / "prompts"
            self._cache_dir.mkdir(parents=True, exist_ok=True)

    def parse(self, prompt: str) -> AppRequirements:
        """
        Parse a natural language prompt into structured requirements.

        Args:
            prompt: Natural language description of the app

        Returns:
            AppRequirements object containing parsed requirements
        """
        # Check cache first for performance optimization
        cached_result = self._get_from_cache(prompt)
        if cached_result:
            if self.config.verbose:
                print("      Using cached parse result")
            return cached_result

        # This is a simplified implementation
        # In production, this would use an LLM to parse the prompt

        # Extract app name from prompt (optimized with early return)
        app_name = self._extract_app_name(prompt)

        # Extract features (optimized to avoid redundant processing)
        features = self._extract_features(prompt)

        result = AppRequirements(
            app_name=app_name,
            description=prompt,
            features=features,
            ui_framework=self.config.ui_framework,
            metadata={"original_prompt": prompt, "language": self.config.language},
        )

        # Cache the result for future use
        self._save_to_cache(prompt, result)

        return result

    def _extract_app_name(self, prompt: str) -> str:
        """Extract or generate app name from prompt."""
        # Simple extraction - look for keywords
        prompt_lower = prompt.lower()

        if "counter" in prompt_lower:
            return "CounterApp"
        elif "weather" in prompt_lower:
            return "WeatherApp"
        elif "todo" in prompt_lower or "task" in prompt_lower:
            return "TodoApp"
        elif "photo" in prompt_lower or "gallery" in prompt_lower:
            return "PhotoGallery"
        else:
            return "GeneratedApp"

    def _extract_features(self, prompt: str) -> List[AppFeature]:
        """Extract features from the prompt."""
        # Simplified feature extraction
        features = []
        prompt_lower = prompt.lower()

        if "counter" in prompt_lower:
            features.append(
                AppFeature(
                    name="Counter",
                    description="Display and modify a counter value",
                    ui_elements=["label", "button", "button"],
                    functionality=["increment", "decrement", "display"],
                )
            )

        if "weather" in prompt_lower:
            features.append(
                AppFeature(
                    name="WeatherDisplay",
                    description="Show weather information",
                    ui_elements=["label", "image", "text"],
                    functionality=[
                        "fetch_weather",
                        "display_temperature",
                        "display_conditions",
                    ],
                )
            )

        if "todo" in prompt_lower or "task" in prompt_lower:
            features.append(
                AppFeature(
                    name="TaskList",
                    description="Manage a list of tasks",
                    ui_elements=["list", "text_field", "button"],
                    functionality=["add_task", "remove_task", "toggle_completion"],
                )
            )

        # If no specific features detected, create a generic feature
        if not features:
            features.append(
                AppFeature(
                    name="MainFeature",
                    description="Main application functionality",
                    ui_elements=["view"],
                    functionality=["display"],
                )
            )

        return features

    def _get_cache_key(self, prompt: str) -> str:
        """Generate a cache key for the prompt."""
        # Create hash of prompt + config settings that affect parsing
        cache_input = f"{prompt}:{self.config.ui_framework}:{self.config.language}"
        return hashlib.sha256(cache_input.encode()).hexdigest()

    def _get_from_cache(self, prompt: str) -> Optional[AppRequirements]:
        """Retrieve parsed requirements from cache if available."""
        cache_key = self._get_cache_key(prompt)

        # Check in-memory cache first (fastest)
        if cache_key in self._cache:
            return self._cache[cache_key]

        # Check disk cache if enabled
        if self._cache_dir:
            cache_file = self._cache_dir / f"{cache_key}.json"
            if cache_file.exists():
                try:
                    with open(cache_file, "r") as f:
                        data = json.load(f)
                    # Reconstruct AppRequirements from cached data
                    features = [AppFeature(**feat) for feat in data["features"]]
                    result = AppRequirements(
                        app_name=data["app_name"],
                        description=data["description"],
                        features=features,
                        ui_framework=data["ui_framework"],
                        metadata=data["metadata"],
                    )
                    # Store in memory cache for faster future access
                    self._cache[cache_key] = result
                    return result
                except (json.JSONDecodeError, KeyError):
                    # Cache corrupted, ignore and reparse
                    pass

        return None

    def _save_to_cache(self, prompt: str, result: AppRequirements):
        """Save parsed requirements to cache."""
        cache_key = self._get_cache_key(prompt)

        # Always save to in-memory cache
        self._cache[cache_key] = result

        # Save to disk cache if enabled
        if self._cache_dir:
            cache_file = self._cache_dir / f"{cache_key}.json"
            try:
                data = {
                    "app_name": result.app_name,
                    "description": result.description,
                    "features": [
                        {
                            "name": f.name,
                            "description": f.description,
                            "ui_elements": f.ui_elements,
                            "functionality": f.functionality,
                        }
                        for f in result.features
                    ],
                    "ui_framework": result.ui_framework,
                    "metadata": result.metadata,
                }
                with open(cache_file, "w") as f:
                    json.dump(data, f, indent=2)
            except Exception:
                # Cache write failed, not critical - continue
                pass
