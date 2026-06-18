from setuptools import setup, find_packages

setup(
    name="repohealth",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "gitpython>=3.1.0",
        "click>=8.1.0",
    ],
    entry_points={
        "console_scripts": [
            "repohealth=repohealth.cli:main",
        ],
    },
    python_requires=">=3.12",
)