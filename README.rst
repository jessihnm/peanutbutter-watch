Berlin Bike Watch
-----------------

Script that scrapes the Berlin Police website and generates a list of
the bikes found by brand.


Motivation
==========

My bike got stolen and I want to keep an eye on the police's findings,
who knows? Maybe I'll recover my bike.


Usage
=====

.. code:: bash

   pipenv install --dev
   pipenv shell

   # then ...
   peanutbutter-watch "https://www.berlin.de/polizei/service/vermissen-sie-ihr-fahrrad/herrenfahrraeder/" -o male-bikes.json
   peanutbutter-watch "https://www.berlin.de/polizei/service/vermissen-sie-ihr-fahrrad/damenfahrraeder/" -o female-bikes.json
   peanutbutter-watch "https://www.berlin.de/polizei/service/vermissen-sie-ihr-fahrrad/kinderfahrraeder/" -o children-bikes.json
   peanutbutter-watch "https://www.berlin.de/polizei/service/vermissen-sie-ihr-fahrrad/sonstige-fahrraeder/" -o misc-bikes.json
   peanutbutter-watch "https://www.berlin.de/polizei/service/vermissen-sie-ihr-fahrrad/fahrradteile/" -o mutilated-bikes.json
