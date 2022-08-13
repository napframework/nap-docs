<br>
<p align="center">
  <img width=384 src="https://download.nap.tech/identity/svg/logos/nap_logo_blue.svg">
</p>

This repository hosts the [NAP technical documentation](https://docs.nap.tech). The docs are auto-generated from [source code](https://github.com/napframework/nap) and published here as a Github page. Documentation is built against the main branch of NAP.

Run the `build.py` script inside the `app` directory to auto-generate system documentation using `Doxygen`. The script clones and pulls the NAP repo if required. The result will be copied into the `docs/html` directory and pushed to `nap-docs`, if the `push-changes` flag is set. Credentials are required to push.

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
