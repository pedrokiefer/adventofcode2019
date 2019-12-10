clean:
	find . -name '__pycache__' | xargs rm -Rf
	find . -name '.pytest_cache' | xargs rm -Rf
	find . -name '*.pyc' | xargs rm -Rf
