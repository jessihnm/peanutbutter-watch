default: dependencies tests run

dependencies:
	pipenv install --dev

tests:
	pipenv run nosetests tests

tdd:
	pipenv run nosetests --with-watch tests/

distribution:
	@python setup.py build sdist

clean:
	@find . -type f -name '*.pyc' -exec rm -f {} \;
	@rm -rf docs/build dist *egg-info*

# tells "make" that the target "make docs" is phony, meaning that make
# should ignore the existence of a file or folder named "docs" and
# simply execute commands described in the target
.PHONY: docs
