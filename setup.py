"""Setup script for NaturalPromptXcode."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="naturalpromptxcode",
    version="0.1.0",
    author="NaturalPromptXcode Team",
    author_email="",
    description="Build iOS applications from natural language prompts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NaTo1000/NaturalPromptXcode",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "pyyaml>=6.0",
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "pylint>=2.17.0",
            "mypy>=1.4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "naturalpromptxcode=main:main",
        ],
    },
)
