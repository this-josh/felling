from setuptools import setup, find_packages

project_urls = {
    "Source": "https://github.com/this-josh/felling",
    "Tracker": "https://github.com/this-josh/felling/issues",
}

with open("README.md", "r") as f:
    long_description = f.read()

classifiers = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: MIT License",
]


setup(
    name="felling",
    description="A simple package to easily create consistent logs",
    author="Josh Kirk",
    author_email="felling@joshkirk.co.uk",
    packages=find_packages(),
    include_package_data=True,
    package_data={"": ["*.json"]},
    url="https://github.com/this-josh/felling",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="logging logs log",
    license="MIT",
    python_requires=">=3.6",
)
