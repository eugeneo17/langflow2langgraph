#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Run Converter Script
-------------------

A simple script to demonstrate the conversion of a LangFlow JSON file to LangGraph Python code.
"""

import os
import sys
from rich.console import Console
from rich.syntax import Syntax

from langflow2langgraph.converter import convert_langflow_to_langgraph

def main():
    """
    Main function to run the converter on a sample flow.
    """
    console = Console()
    
    # Path to the sample flow
    sample_input = "drdemo"
    sample_path = os.path.join("input_flows", f'{sample_input}'+ '.json')
    #sample_path = os.path.join("input_flows", "agent_example.json")
    
    # Check if the sample file exists
    if not os.path.isfile(sample_path):
        console.print(f"[bold red]Error:[/] Sample file '{sample_path}' not found")
        return 1
    
    # Convert the sample flow
    console.print(f"Converting sample flow: [bold cyan]{sample_path}[/]")
    
    try:
        # Generate the code
        generated_code = convert_langflow_to_langgraph(sample_path)
        
        # Print the generated code with syntax highlighting
        syntax = Syntax(
            generated_code,
            "python",
            theme="monokai",
            line_numbers=True,
            word_wrap=True
        )
        console.print(syntax)
        
        # Optionally save the generated code
        output_path = os.path.join("output_graphs", f'{sample_input}'+ '.py')
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(generated_code)
        
        console.print(f"[bold green]Success![/] Generated code saved to [bold cyan]{output_path}[/]")
        
        return 0
    
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
