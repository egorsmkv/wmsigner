PYTHON=python3

test:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py'

clean:
	find . -name "*.py[oc]" -delete
	find . -name "__pycache__" -delete
	rm -rf build dist MANIFEST

pypi: clean
	$(PYTHON) setup.py sdist upload
