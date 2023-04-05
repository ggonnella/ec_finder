.PHONY: manual cleanup upload sdist wheel install

PYTHON=python3
PIP=pip3

# Install using pip
install:
	${PIP} install --upgrade --user --editable .

# Source distribution
sdist:
	${PYTHON} setup.py sdist

# Pure Python Wheel
wheel:
	${PYTHON} setup.py bdist_wheel

# Remove distribution files
cleanup:
	rm -rf dist/ build/ *.egg-info/

tests:
	pytest

testcov:
	pip install pytest-cov -qqq
	pytest -v --cov=ec_finder --cov=bin \
		     --cov-report=html \
		     tests/

upload: cleanup sdist wheel
	cd dist; \
  	for file in *; do \
		  twine check $$file && \
		  twine upload $$file; \
		done
