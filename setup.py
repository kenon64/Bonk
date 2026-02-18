"""
Setup script для установки Bonk.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bonk",
    version="1.0.0",
    author="Bonk Team",
    description="Audio to MIDI converter - преобразование аудиофайлов в нотную запись",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kenon64/Bonk",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "librosa>=0.10.0",
        "numpy>=1.24.0",
        "scipy>=1.11.0",
        "pretty_midi>=0.2.10",
        "soundfile>=0.12.1",
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "bonk=bonk.cli:cli",
        ],
    },
    include_package_data=True,
)
