from setuptools import setup, find_packages

setup(
    name="easy_logger",
    version="0.1",
    description="A simple package to easily create consistent logs",
    author="Josh Kirk",
    author_email="-",
    packages=find_packages(),
    package_data={"": ["*.json"]},
)
