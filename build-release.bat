@echo off
pip install --upgrade setuptools wheel twine
python setup.py sdist bdist_wheel
rem Test PyPi
rem twine upload --repository-url https://test.pypi.org/legacy/ dist/*
rem Prod PyPi
twine upload dist/*