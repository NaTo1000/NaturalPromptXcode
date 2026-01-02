"""
NaturalPromptXcode - Build iOS apps from natural language prompts

Main entry point for the command-line interface.
"""

import argparse
import sys
import os
from pathlib import Path

from .nlp.parser import PromptParser
from .codegen.generator import CodeGenerator
from .builder.xcode import XcodeProjectBuilder
from .config import Config
from .security.cli import add_security_commands


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Build iOS applications from natural language prompts",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Default command: generate (for backward compatibility)
    generate_parser = subparsers.add_parser(
        'generate',
        help='Generate iOS app from natural language prompt'
    )
    
    generate_parser.add_argument(
        "prompt",
        type=str,
        help="Natural language description of the app to build"
    )
    
    generate_parser.add_argument(
        "--output-dir",
        type=str,
        default="./output",
        help="Directory to save generated project (default: ./output)"
    )
    
    generate_parser.add_argument(
        "--language",
        type=str,
        choices=["swift", "objective-c"],
        default="swift",
        help="Target language (default: swift)"
    )
    
    generate_parser.add_argument(
        "--ui-framework",
        type=str,
        choices=["swiftui", "uikit"],
        default="swiftui",
        help="UI framework (default: swiftui)"
    )
    
    generate_parser.add_argument(
        "--model",
        type=str,
        default="gpt-4",
        help="AI model to use (default: gpt-4)"
    )
    
    generate_parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    generate_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate code without building"
    )
    
    # Add security commands
    add_security_commands(subparsers)
    
    # Parse arguments
    args = parser.parse_args()
    
    # Handle security commands
    if hasattr(args, 'func'):
        return args.func(args)
    
    # If no command specified, treat first arg as prompt for backward compatibility
    if args.command is None:
        # Backward compatibility: if no subcommand, assume generate
        if len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
            # Parse again with generate as default
            sys.argv.insert(1, 'generate')
            args = parser.parse_args()
        else:
            parser.print_help()
            return 1
    
    # Handle generate command
    if args.command != 'generate':
        parser.print_help()
        return 1
    
    # Load configuration
    config = Config()
    config.model_name = args.model
    config.ui_framework = args.ui_framework
    config.language = args.language
    config.verbose = args.verbose
    
    if args.verbose:
        print(f"NaturalPromptXcode - Building iOS app from prompt")
        print(f"Prompt: {args.prompt}")
        print(f"Output: {args.output_dir}")
        print(f"Framework: {args.ui_framework}")
        print(f"Model: {args.model}")
        print()
    
    try:
        # Parse prompt
        if args.verbose:
            print("[1/4] Parsing natural language prompt...")
        
        prompt_parser = PromptParser(config)
        requirements = prompt_parser.parse(args.prompt)
        
        if args.verbose:
            print(f"      Identified {len(requirements.features)} features")
        
        # Generate code
        if args.verbose:
            print("[2/4] Generating iOS code...")
        
        code_generator = CodeGenerator(config)
        project_structure = code_generator.generate(requirements)
        
        if args.verbose:
            print(f"      Generated {len(project_structure.files)} files")
        
        # Create Xcode project
        if args.verbose:
            print("[3/4] Creating Xcode project...")
        
        builder = XcodeProjectBuilder(config)
        project_path = builder.create_project(
            project_structure,
            output_dir=args.output_dir
        )
        
        if args.verbose:
            print(f"      Project created at: {project_path}")
        
        # Build project (unless dry-run)
        if not args.dry_run:
            if args.verbose:
                print("[4/4] Building project...")
            
            app_path = builder.build(project_path)
            
            if args.verbose:
                print(f"      App built successfully: {app_path}")
        else:
            if args.verbose:
                print("[4/4] Skipping build (dry-run mode)")
        
        print()
        print("✓ Success! Your iOS app is ready.")
        print(f"  Project: {project_path}")
        
        if not args.dry_run:
            print(f"  App: {app_path}")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        return 130
    
    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
