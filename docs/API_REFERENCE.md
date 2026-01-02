# API Reference

## Command Line Interface

### Main Command

```bash
python naturalpromptxcode.py [OPTIONS] PROMPT
```

#### Arguments

- `PROMPT`: Natural language description of the app to build (required)

#### Options

- `--output-dir PATH`: Directory to save generated project (default: `./output`)
- `--language LANG`: Target language, either `swift` or `objective-c` (default: `swift`)
- `--ui-framework FRAMEWORK`: UI framework, either `swiftui` or `uikit` (default: `swiftui`)
- `--model MODEL`: AI model to use (default: `gpt-4`)
- `--verbose`: Enable verbose output
- `--dry-run`: Generate code without building

#### Examples

```bash
# Basic usage
python naturalpromptxcode.py "Create a todo list app"

# With options
python naturalpromptxcode.py "Create a photo gallery app" \
  --output-dir ~/Projects/PhotoApp \
  --ui-framework uikit \
  --verbose
```

## Python API

### NaturalPromptXcode Class

Main class for programmatic access.

```python
from naturalpromptxcode import NaturalPromptXcode

# Initialize
builder = NaturalPromptXcode(
    model="gpt-4",
    ui_framework="swiftui"
)

# Generate app
project = builder.generate(
    prompt="Create a weather app",
    output_dir="./output"
)

# Build app
app_path = builder.build(project)
```

### Methods

#### `generate(prompt, output_dir=None, **kwargs)`

Generate iOS project from natural language prompt.

**Parameters:**
- `prompt` (str): Natural language description
- `output_dir` (str, optional): Output directory path
- `**kwargs`: Additional generation options

**Returns:**
- `Project`: Project object representing the generated Xcode project

#### `build(project, configuration="Debug")`

Build the generated iOS project.

**Parameters:**
- `project` (Project): Project to build
- `configuration` (str): Build configuration ("Debug" or "Release")

**Returns:**
- `str`: Path to built application

#### `validate_prompt(prompt)`

Validate if a prompt can be processed.

**Parameters:**
- `prompt` (str): Prompt to validate

**Returns:**
- `dict`: Validation result with `valid` (bool) and `issues` (list)

### Project Class

Represents a generated Xcode project.

```python
class Project:
    def __init__(self, path, name):
        self.path = path
        self.name = name
        self.files = []
    
    def add_file(self, file_path, content):
        """Add a file to the project"""
        pass
    
    def save(self):
        """Save project to disk"""
        pass
```

## Configuration

### config.yaml

```yaml
# AI Model Configuration
model:
  provider: "openai"  # or "local"
  name: "gpt-4"
  temperature: 0.7
  max_tokens: 2000

# Build Configuration
build:
  default_framework: "swiftui"
  default_language: "swift"
  target_ios_version: "15.0"

# Output Configuration
output:
  default_dir: "./output"
  clean_before_build: true
```

## Error Codes

| Code | Description |
|------|-------------|
| 100 | Invalid prompt |
| 101 | Model initialization failed |
| 200 | Code generation failed |
| 201 | Invalid code structure |
| 300 | Project creation failed |
| 301 | Build failed |
| 400 | Configuration error |

## Events and Hooks

### Event Callbacks

```python
def on_generation_start(prompt):
    print(f"Generating from: {prompt}")

def on_generation_complete(project):
    print(f"Generated project: {project.name}")

builder = NaturalPromptXcode()
builder.on("generation_start", on_generation_start)
builder.on("generation_complete", on_generation_complete)
```
