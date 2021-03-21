# How to release PYPI
1. Ensure branch is clean
2. `git tag felling-{version}`, ensuring `{version}` has all 3 numerical values, e.g. `1.0.0`
4. `python -m build` builds the package
5. Optional: Upload package to testpypi, check all is okay `twine upload --repository testpypi dist/*` 
6. `git push; git push --tags` to push tags to github
7. [Create a new release](https://github.com/this-josh/felling/releases/new) enter the previously chosen tag, upload the resources produced by `python -m build`
8. `twine upload dist/*` to update the package in pypi

# How to release Conda Forge
1. Fork [Felling feedstock](https://github.com/conda-forge/felling-feedstock)
2. Update the version number and SHA256 in `recipe/meta.yaml`
3. Submit a pull request