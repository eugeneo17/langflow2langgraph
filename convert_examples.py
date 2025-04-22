#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from langgraph2langflow import convert_langflow_to_langgraph

def main():
    # Create examples directory if it doesn't exist
    if not os.path.exists("examples"):
        os.makedirs("examples")

    # Create input_flows and output_graphs directories if they don't exist
    if not os.path.exists("input_flows"):
        os.makedirs("input_flows")
    if not os.path.exists("output_graphs"):
        os.makedirs("output_graphs")

    # Skip conversion if files already exist
    # Convert loop flow
    loop_input = "input_flows/loop_flow.json"
    loop_output = "output_graphs/loop_graph.py"

    if not os.path.exists(loop_output):
        print(f"Converting loop flow: {loop_input} -> {loop_output}")
        loop_code = convert_langflow_to_langgraph(loop_input, loop_output, validate=True)
        print(f"Successfully converted loop flow")
    else:
        print(f"Skipping conversion of loop flow - {loop_output} already exists")

    # Convert conditional flow
    cond_input = "input_flows/conditional_flow.json"
    cond_output = "output_graphs/conditional_graph.py"

    if not os.path.exists(cond_output):
        print(f"Converting conditional flow: {cond_input} -> {cond_output}")
        cond_code = convert_langflow_to_langgraph(cond_input, cond_output, validate=True)
        print(f"Successfully converted conditional flow")
    else:
        print(f"Skipping conversion of conditional flow - {cond_output} already exists")

    # Convert simple chat flow
    chat_input = "input_flows/simple_chat.json"
    chat_output = "output_graphs/simple_chat.py"

    if not os.path.exists(chat_output):
        print(f"Converting simple chat flow: {chat_input} -> {chat_output}")
        chat_code = convert_langflow_to_langgraph(chat_input, chat_output, validate=True)
        print(f"Successfully converted simple chat flow")
    else:
        print(f"Skipping conversion of simple chat flow - {chat_output} already exists")

    # Convert retrieval QA flow
    qa_input = "input_flows/retrieval_qa.json"
    qa_output = "output_graphs/retrieval_qa.py"

    if not os.path.exists(qa_output):
        print(f"Converting retrieval QA flow: {qa_input} -> {qa_output}")
        qa_code = convert_langflow_to_langgraph(qa_input, qa_output, validate=True)
        print(f"Successfully converted retrieval QA flow")
    else:
        print(f"Skipping conversion of retrieval QA flow - {qa_output} already exists")

    # Convert agent flow
    agent_input = "input_flows/agent_example.json"
    agent_output = "output_graphs/agent_graph.py"

    if not os.path.exists(agent_output):
        print(f"Converting agent flow: {agent_input} -> {agent_output}")
        agent_code = convert_langflow_to_langgraph(agent_input, agent_output, validate=True)
        print(f"Successfully converted agent flow")
    else:
        print(f"Skipping conversion of agent flow - {agent_output} already exists")

    # Run tests
    print("\nRunning tests...")

    print("\nTesting loop graph:")
    os.system("python test_loop_graph.py")

    print("\nTesting conditional graph:")
    os.system("python test_conditional_graph.py")

    return 0

if __name__ == "__main__":
    sys.exit(main())
