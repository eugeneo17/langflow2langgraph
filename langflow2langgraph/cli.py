#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
LangFlow to LangGraph CLI
-------------------------

Command-line interface for converting LangFlow JSON exports to LangGraph Python code.
"""

import argparse
import os
import sys
from typing import Optional, List

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from langflow2langgraph.converter import convert_langflow_to_langgraph


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parse command line arguments.
    
    Args:
        args: Command line arguments (defaults to sys.argv[1:])
        
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Convert LangFlow JSON exports to LangGraph Python code",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "input_file",
        help="Path to the LangFlow JSON file"
    )
    
    parser.add_argument(
        "--output", "-o",
        help="Path to save the generated Python code (if not provided, prints to stdout)"
    )
    
    parser.add_argument(
        "--preview", "-p",
        action="store_true",
        help="Preview the generated code without saving"
    )
    
    return parser.parse_args(args)


def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for the CLI.
    
    Args:
        args: Command line arguments (defaults to sys.argv[1:])
        
    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    console = Console()
    
    try:
        parsed_args = parse_args(args)
        
        # Check if input file exists
        if not os.path.isfile(parsed_args.input_file):
            console.print(f"[bold red]Error:[/] Input file '{parsed_args.input_file}' not found")
            return 1
        
        # Convert the file
        console.print(f"Converting [bold cyan]{parsed_args.input_file}[/]...")
        
        generated_code = convert_langflow_to_langgraph(
            parsed_args.input_file,
            None if parsed_args.preview else parsed_args.output
        )
        
        # Handle output
        if parsed_args.preview or not parsed_args.output:
            # Print the generated code with syntax highlighting
            syntax = Syntax(
                generated_code,
                "python",
                theme="monokai",
                line_numbers=True,
                word_wrap=True
            )
            console.print(Panel(
                syntax,
                title="Generated LangGraph Code",
                expand=False
            ))
            
            if not parsed_args.output:
                console.print("[yellow]Note:[/] No output file specified. Use --output to save the code.")
        else:
            console.print(f"[bold green]Success![/] Generated code saved to [bold cyan]{parsed_args.output}[/]")
        
        return 0
        
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
