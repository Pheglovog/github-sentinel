#!/usr/bin/env python3
"""
GitHub Sentinel - Main entry point

Quick start examples:
    python main.py --help
    python main.py status
    python main.py analyze -r microsoft/vscode
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import and run the CLI
from github_sentinel.cli.commands import main

if __name__ == "__main__":
    main()
