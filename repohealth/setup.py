from pathlib import Path

from setuptools import setup

version_ns = {}
exec((Path(__file__).parent / "__init__.py").read_text(), version_ns)

setup(
    name="repohealth",
    version=version_ns["__version__"],
    packages=["repohealth", "repohealth.tests"],
    package_dir={"repohealth": "."},
    install_requires=[
        "gitpython>=3.1.0",
        "click>=8.1.0",
    ],
    entry_points={
        "console_scripts": [
            "repohealth=repohealth.cli:main",
        ],
    },
    python_requires=">=3.11",
)