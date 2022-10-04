@echo off
pip install --upgrade setuptools wheel twine
python setup.py sdist bdist_wheel
# Test PyPi
#twine upload --repository-url https://test.pypi.org/legacy/ dist/*
# Prod PyPi
twine upload dist/*