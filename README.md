[![Build Status](https://travis-ci.org/FabienArcellier/blueprint-webapp-flask.svg?branch=master)](https://travis-ci.org/FabienArcellier/blueprint-webapp-flask)

# Onze de légende

> Application which makes it possible to compose the best current football team.

## Getting started

### System requirements

The following requirements has to be setup on your host before running the command
from this repository.

* `python 3.6` at least

You may have an IDE in order to check the .html and .css packages.

## The latest version

You can find the latest version to ...

```bash
git clone git@github.com:JulienPetit-1/DataTools_Project.git
```

## Usage

You can access to our website with the following url :
(Insérer URL)

On this website, you can find dataframes with players and clubs from the lastest football season. 
The dataframe is composed as follows : 

| Name | Club | Cost | Position | Goals | Minutes played | Matchs | Redcard | ROI |
| :------: | :------: | :------: | :------: | :------: | :------: | :------: | :------: |:------:|
| player1 | club1 | M€ | position1 | x | x | x | x | x |

>ROI stands for Return On Investment

Check below the caracteristics that you can choose on the home page in order to find the good football team you want :

* Your budget 
* The maximum number of football's stars in your team
* The maximum number of goalkeepers in your team
* The maximum number of defenders in your team
* The maximum number of middlekeepers in your team
* The maximum number of attackers in your team

You will find on the desktop-hd screen a field with the 11 best players of the moment.


### Install development environment

Use make to instanciate a python virtual environment in ./venv3 and install the
python dependencies.

```bash
make install_requirements_dev
```

### Run the linter and the unit tests

Before commit or send a pull request, you have to execute pylint to check the syntax
of your code and run the unit tests to validate the behavior.

```bash
make lint
make tests
```

## Ressources

Images and data come from a logistic football website. 

>Link : https://fr.soccerway.com/

## Built With

[Visual Stucio Code](https://code.visualstudio.com/) - Html/css 
[Python 3.8](https://www.python.org/) - Backend


## Contributing

Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests to us.

## Contributors

* Rodolphe MATHIEU
* Raphaël PORTELL
* Julien PETIT
