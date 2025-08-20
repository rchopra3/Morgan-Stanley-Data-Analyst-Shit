#!/usr/bin/env python3
"""
Setup script for Morgan Stanley Global Markets Analytics
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
    return long_description

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    return requirements

setup(
    name="morgan-stanley-analytics",
    version="1.0.0",
    author="Morgan Stanley Global Markets Analytics",
    author_email="analytics@morganstanley.com",
    description="Comprehensive financial analytics framework for portfolio analysis, risk management, and compliance monitoring",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/morgan-stanley-analytics",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/morgan-stanley-analytics/issues",
        "Documentation": "https://github.com/yourusername/morgan-stanley-analytics#readme",
        "Source Code": "https://github.com/yourusername/morgan-stanley-analytics",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
            "pre-commit>=2.20.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "myst-parser>=0.18.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ms-analytics=morgan_stanley_analytics.main_analytics:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md", "*.yml", "*.yaml"],
    },
    keywords=[
        "financial",
        "analytics",
        "portfolio",
        "risk",
        "compliance",
        "trading",
        "investment",
        "var",
        "stress-testing",
        "performance",
        "attribution",
        "morgan-stanley",
        "banking",
        "quantitative",
    ],
    platforms=["any"],
    zip_safe=False,
)
