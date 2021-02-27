from setuptools import setup, find_packages

setup(
    name="felling",
    version="0.0.1rc1",
    description="A simple package to easily create consistent logs",
    author="Josh Kirk",
    author_email="felling@joshkirk.co.uk",
    packages=find_packages(),
    package_data={"": ["*.json"]},
)
