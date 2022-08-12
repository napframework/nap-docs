<br>
<p align="center">
  <img width=384 src="https://download.nap.tech/identity/svg/logos/nap_logo_blue.svg">
</p>

This repository builds and hosts the NAP technical documentation. The docs are auto-generated from [source code](https://github.com/napframework/nap) and published here as a Github page. Documentation is guaranteed to be in-sync with the latest official [NAP release](https://github.com/napframework/nap/releases). 

Run the `build.py` script inside the `app` directory to auto-generate system documentation using `Doxygen`. The script clones and pulls the NAP repo if required. The result will be copied into the `docs/html` directory and pushed to `nap-docs`. Credentials are required to push.

## Dependencies
- [Python (3.8+)](https://www.python.org/downloads/) 
- [pip](https://pypi.org/project/pip/)
- [doxygen](https://doxygen.nl/)
- [graphviz](https://graphviz.org/)
- [git](https://git-scm.com/)

## Installation
Create a virtual python environment for the project and install all required python dependencies:

```shell
$ pip install --user pipenv
$ cd nap-docs
$ pipenv install
```

## Build
Generate a static version of the website:
```shell
$ pipenv shell
$ cd app
$ python build.py
$ exit
```