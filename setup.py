from setuptools import setup, find_packages

project_urls = {
    "Source": "https://github.com/this-josh/felling",
    "Tracker": "https://github.com/this-josh/felling/issues",
}

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="felling",
    version="0.0.1rc2",
    description="A simple package to easily create consistent logs",
    author="Josh Kirk",
    author_email="felling@joshkirk.co.uk",
    packages=find_packages(),
    package_data={"": ["*.json"]},
    url="https://github.com/this-josh/felling",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="logging logs log",
    license="MIT",
)
