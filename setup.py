from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mandarin-english-reader",
    version="0.1.0",
    author="Liem Nguyen",
    description="A PDF generator that creates bilingual documents using Lingtrain Aligner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "lingtrain-aligner>=0.4.0",
        "PyPDF2>=3.0.0",
        "ebooklib>=0.18",
        "reportlab>=4.0.0",
        "beautifulsoup4>=4.12.0",
        "lxml>=4.9.0",
        "click>=8.1.0",
    ],
    entry_points={
        "console_scripts": [
            "bilingual-pdf=bilingual_reader.cli:main",
        ],
    },
)
