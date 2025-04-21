#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from langgraph2langflow import convert_langflow_to_langgraph

def main():
    # Create examples directory if it doesn't exist
    if not os.path.exists("examples"):
        os.makedirs("examples")

    # Skip conversion if files already exist
    # Convert loop flow
    loop_input = "examples/loop_flow.json"
    loop_output = "generated_loop_graph.py"

    if not os.path.exists(loop_output):
        print(f"Converting loop flow: {loop_input} -> {loop_output}")
        loop_code = convert_langflow_to_langgraph(loop_input, loop_output, validate=True)
        print(f"Successfully converted loop flow")
    else:
        print(f"Skipping conversion of loop flow - {loop_output} already exists")

    # Convert conditional flow
    cond_input = "examples/conditional_flow.json"
    cond_output = "generated_conditional_graph.py"

    if not os.path.exists(cond_output):
        print(f"Converting conditional flow: {cond_input} -> {cond_output}")
        cond_code = convert_langflow_to_langgraph(cond_input, cond_output, validate=True)
        print(f"Successfully converted conditional flow")
    else:
        print(f"Skipping conversion of conditional flow - {cond_output} already exists")

    # Run tests
    print("\nRunning tests...")

    print("\nTesting loop graph:")
    os.system("python test_loop_graph.py")

    print("\nTesting conditional graph:")
    os.system("python test_conditional_graph.py")

    return 0

if __name__ == "__main__":
    sys.exit(main())
