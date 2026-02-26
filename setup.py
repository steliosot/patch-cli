from setuptools import setup

setup(
    name="patch-cli",
    version="1.0.0",
    author="steliosot",
    author_email="",
    description="A CLI tool that automatically fixes broken shell commands using OpenAI GPT-4o-mini",
    url="https://github.com/steliosot/patch-cli",
    py_modules=["patch"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "openai",
        "tqdm",
    ],
    entry_points={
        "console_scripts": [
            "patch=patch:main",
        ],
    },
)