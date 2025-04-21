#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="langflow2langgraph",
    version="0.1.0",
    description="Convert LangFlow JSON exports into LangGraph Python code",
    author="Neuronaut",
    author_email="neuronaut73@users.noreply.github.com",
    url="https://github.com/neuronaut73/langflow2langgraph",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "langchain>=0.1.0",
        "rich",
    ],
    extras_require={
        "openai": ["openai"],
    },
    entry_points={
        "console_scripts": [
            "lf2lg=langflow2langgraph.cli:main"
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="langflow, langgraph, langchain, converter",
)
