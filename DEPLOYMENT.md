# Deployment of Pypi package

The pypi package is deployment is managed via a github action.
To make a new release:
1. Increment version number in `src/nrsur_catalog/__init__.py`
2. Edit the `CHANGELOG.md`
3. Make a `tagged` commit (tag with `VX.Y.Z`) to the `main` branch


