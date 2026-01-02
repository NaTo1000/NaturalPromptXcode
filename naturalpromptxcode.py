#!/usr/bin/env python3
"""
Command-line wrapper for NaturalPromptXcode.
This script can be run directly from the repository.
"""

import sys
import os

# Add parent directory to path for development usage
parent_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(parent_dir, 'src')
if os.path.exists(src_path) and src_path not in sys.path:
    sys.path.insert(0, parent_dir)

# Import and run the main function
if __name__ == "__main__":
    from src.main import main
    sys.exit(main())
