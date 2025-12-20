# Model Configuration Examples

## Configuration File: config.yaml

```yaml
# AI Model Configuration
model:
  provider: "openai"        # Options: openai, local, anthropic
  name: "gpt-4"            # Model name/identifier
  temperature: 0.7          # Creativity vs consistency (0.0-1.0)
  max_tokens: 2000         # Maximum response length
  
  # Optional: API configuration
  api_key_env: "OPENAI_API_KEY"
  api_base: "https://api.openai.com/v1"
  
  # Optional: Timeout settings
  timeout: 30
  max_retries: 3

# Build Configuration
build:
  default_framework: "swiftui"    # swiftui or uikit
  default_language: "swift"       # swift or objective-c
  target_ios_version: "15.0"
  
# Output Configuration
output:
  default_dir: "./output"
  clean_before_build: true
  preserve_metadata: true
```

## OpenAI Configuration

```yaml
model:
  provider: "openai"
  name: "gpt-4-turbo-preview"
  temperature: 0.7
  max_tokens: 4096
  api_key_env: "OPENAI_API_KEY"
```

## Local LLM Configuration

```yaml
model:
  provider: "local"
  name: "codellama-13b"
  model_path: "./models/codellama-13b.gguf"
  temperature: 0.5
  max_tokens: 2048
  gpu_layers: 35          # Number of layers to offload to GPU
  context_length: 4096
```

## Anthropic Claude Configuration

```yaml
model:
  provider: "anthropic"
  name: "claude-3-opus-20240229"
  temperature: 0.7
  max_tokens: 4096
  api_key_env: "ANTHROPIC_API_KEY"
```

## Environment Variables

Set up your environment with appropriate credentials:

```bash
# OpenAI
export OPENAI_API_KEY="sk-..."

# Anthropic
export ANTHROPIC_API_KEY="sk-ant-..."

# Custom endpoint (optional)
export NPX_API_ENDPOINT="https://custom-api.example.com"

# Model override (optional)
export NPX_MODEL="gpt-4"
```

## Model Selection Guide

### For Simple Apps (Counter, Calculator)
```yaml
model:
  name: "gpt-3.5-turbo"
  temperature: 0.5
  max_tokens: 1000
```

### For Complex Apps (Multi-screen, Network, Data)
```yaml
model:
  name: "gpt-4"
  temperature: 0.7
  max_tokens: 3000
```

### For Production Use
```yaml
model:
  name: "gpt-4-turbo"
  temperature: 0.6
  max_tokens: 4096
  max_retries: 5
  timeout: 60
```

## Advanced Configuration

### Custom Prompt Templates

```yaml
prompts:
  system_template: |
    You are an expert iOS developer. Generate production-quality
    Swift code following Apple's best practices.
  
  user_template: |
    Create an iOS app with the following requirements:
    {requirements}
    
    Generate SwiftUI code using iOS {ios_version}.
  
  few_shot_examples:
    - prompt: "Create a counter app"
      response: "// Counter app implementation..."
```

### Caching Configuration

```yaml
cache:
  enabled: true
  directory: "./.cache/npx"
  ttl: 3600  # Cache results for 1 hour
  max_size: 100  # Max cached responses
```

## Performance Tuning

### For Speed
```yaml
model:
  name: "gpt-3.5-turbo"
  max_tokens: 1500
  stream: true  # Stream responses
```

### For Quality
```yaml
model:
  name: "gpt-4"
  temperature: 0.6
  max_tokens: 4096
  top_p: 0.95
```

### For Cost Optimization
```yaml
model:
  name: "gpt-3.5-turbo"
  max_tokens: 2000
  cache:
    enabled: true
  retry_with_fallback: true
  fallback_model: "gpt-3.5-turbo"
```
