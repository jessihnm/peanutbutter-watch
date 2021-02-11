.PHONY: all tests dependencies unit functional tdd-functional tdd-unit run clean black

PACKAGE_PATH		:= ./berlin_bike_watch
MAIN_CLI_NAME		:= berlin-bike-watch
GIT_ROOT		:= $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
VENV_ROOT		:= $(GIT_ROOT)/.venv
MAIN_CLI_PATH		:= $(VENV_ROOT)/$(MAIN_CLI_NAME)
export VENV		?= $(VENV_ROOT)
CLI_COMMAND		:= $(VENV)/bin/$(MAIN_CLI_NAME)

all: dependencies tests

venv $(VENV):  # creates $(VENV) folder if does not exist
	python3 -mvenv $(VENV)
	$(VENV)/bin/pip install -U pip setuptools

develop $(MAIN_CLI_PATH) $(VENV)/bin/nosetests $(VENV)/bin/python $(VENV)/bin/pip: # installs latest pip
	test -e $(VENV)/bin/pip || $(MAKE) $(VENV)
	$(VENV)/bin/pip install -r development.txt
	$(VENV)/bin/python setup.py develop

# Runs the unit and functional tests
tests: unit functional  # runs all tests


# Install dependencies
dependencies: | $(VENV)/bin/nosetests
	$(VENV)/bin/pip install -r development.txt
	$(VENV)/bin/python setup.py develop


# runs unit tests
unit: | $(VENV)/bin/nosetests  # runs only unit tests
	$(VENV)/bin/nosetests --cover-erase tests/unit


# runs functional tests
functional:| $(VENV)/bin/nosetests  # runs functional tests
	$(VENV)/bin/nosetests tests/functional

run: | $(VENV)/bin/python
	@$(MAIN_CLI_PATH) --help

clean:
	rm -rf .venv

black:
	black -l 79 $(PACKAGE_PATH) tests

run:
	$(CLI_COMMAND) "https://www.berlin.de/polizei/service/vermissen-sie-ihr-fahrrad/herrenfahrraeder/" -o male-bikes-$$(date +"%Y%m%d-%H%M").json
	$(CLI_COMMAND) "https://www.berlin.de/polizei/service/vermissen-sie-ihr-fahrrad/damenfahrraeder/" -o female-bikes-$$(date +"%Y%m%d-%H%M").json
	$(CLI_COMMAND) "https://www.berlin.de/polizei/service/vermissen-sie-ihr-fahrrad/kinderfahrraeder/" -o children-bikes-$$(date +"%Y%m%d-%H%M").json
	$(CLI_COMMAND) "https://www.berlin.de/polizei/service/vermissen-sie-ihr-fahrrad/sonstige-fahrraeder/" -o misc-bikes-$$(date +"%Y%m%d-%H%M").json
	$(CLI_COMMAND) "https://www.berlin.de/polizei/service/vermissen-sie-ihr-fahrrad/fahrradteile/" -o mutilated-bikes-$$(date +"%Y%m%d-%H%M").json
