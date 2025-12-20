"""Natural Language Processing module for prompt parsing."""

from typing import List, Dict, Any
from dataclasses import dataclass


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
    
    def parse(self, prompt: str) -> AppRequirements:
        """
        Parse a natural language prompt into structured requirements.
        
        Args:
            prompt: Natural language description of the app
            
        Returns:
            AppRequirements object containing parsed requirements
        """
        # This is a simplified implementation
        # In production, this would use an LLM to parse the prompt
        
        # Extract app name from prompt
        app_name = self._extract_app_name(prompt)
        
        # Extract features
        features = self._extract_features(prompt)
        
        return AppRequirements(
            app_name=app_name,
            description=prompt,
            features=features,
            ui_framework=self.config.ui_framework,
            metadata={
                "original_prompt": prompt,
                "language": self.config.language
            }
        )
    
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
            features.append(AppFeature(
                name="Counter",
                description="Display and modify a counter value",
                ui_elements=["label", "button", "button"],
                functionality=["increment", "decrement", "display"]
            ))
        
        if "weather" in prompt_lower:
            features.append(AppFeature(
                name="WeatherDisplay",
                description="Show weather information",
                ui_elements=["label", "image", "text"],
                functionality=["fetch_weather", "display_temperature", "display_conditions"]
            ))
        
        if "todo" in prompt_lower or "task" in prompt_lower:
            features.append(AppFeature(
                name="TaskList",
                description="Manage a list of tasks",
                ui_elements=["list", "text_field", "button"],
                functionality=["add_task", "remove_task", "toggle_completion"]
            ))
        
        # If no specific features detected, create a generic feature
        if not features:
            features.append(AppFeature(
                name="MainFeature",
                description="Main application functionality",
                ui_elements=["view"],
                functionality=["display"]
            ))
        
        return features
