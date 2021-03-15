# How to release
1. Ensure branch is clean
2. `git tag felling-{version}`, ensuring `{version}` has all 3 numerical values, e.g. `1.0.0`
4. `python -m build` builds the package
5. Optional: Upload pacakge to testpypi, check all is okay `twine upload --repository testpypi dist/*` 
6. `git push; git push --tags` to push tags to github
7. [Create a new release](https://github.com/this-josh/felling/releases/new) enter the previously chosen tag, upload the resources produced by `python -m build`
8. `twine upload dist/*` to update the package in pypi