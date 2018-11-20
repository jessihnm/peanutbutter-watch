default: Pipfile.lock tests run

Pipfile.lock:
	pipenv install --dev

tests:
	pipenv run nosetests tests

tdd:
	pipenv run nosetests --with-watch tests/

run: Pipfile.lock
	pipenv run berlin-bike-watch "https://www.berlin.de/polizei/service/vermissen-sie-ihr-fahrrad/herrenfahrraeder/" -o male-bikes-$$(date +"%Y%m%d-%H%M").json
	pipenv run berlin-bike-watch "https://www.berlin.de/polizei/service/vermissen-sie-ihr-fahrrad/damenfahrraeder/" -o female-bikes-$$(date +"%Y%m%d-%H%M").json
	pipenv run berlin-bike-watch "https://www.berlin.de/polizei/service/vermissen-sie-ihr-fahrrad/kinderfahrraeder/" -o children-bikes-$$(date +"%Y%m%d-%H%M").json
	pipenv run berlin-bike-watch "https://www.berlin.de/polizei/service/vermissen-sie-ihr-fahrrad/sonstige-fahrraeder/" -o misc-bikes-$$(date +"%Y%m%d-%H%M").json
	pipenv run berlin-bike-watch "https://www.berlin.de/polizei/service/vermissen-sie-ihr-fahrrad/fahrradteile/" -o mutilated-bikes-$$(date +"%Y%m%d-%H%M").json

distribution:
	@python setup.py build sdist

clean:
	@find . -type f -name '*.pyc' -exec rm -f {} \;
	@rm -rf docs/build dist *egg-info*

# tells "make" that the target "make docs" is phony, meaning that make
# should ignore the existence of a file or folder named "docs" and
# simply execute commands described in the target
.PHONY: docs
