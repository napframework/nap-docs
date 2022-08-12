<br>
<p align="center">
  <img width=384 src="https://download.nap.tech/identity/svg/logos/nap_logo_blue.svg">
</p>

This repository hosts the NAP technical documentation. The docs are auto-generated from [source code](https://github.com/napframework/nap) and published here as a Github page. Documentation is guaranteed to be in-sync with the latest official [NAP release](https://github.com/napframework/nap/releases). 

Run the `generate_documentation.bat` script inside the `docs\doxygen` directory of [NAP Framework](https://github.com/napframework/nap) to auto-generate system documentation using `Doxygen`. The result will be stored in the `docs\html` directory, one level up from `docs\doxygen`. 

The script depends on `python`, `CMake` and [GraphViz](https://graphviz.org/download/). If you want to generate documentation on `unix` based systems you must install `doxygen` as well. Do not remove the `additional_content` directory and `CNAME` file when copying over the generated documentation into `docs`.
