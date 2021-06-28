Materials for my contribution to Lawrence et al. 2021
============

Code:
-------------------------
-------------
The scripts to download and process the data and plot the results are provided. The organization of this project follows loosely from the [cookiecutter-science-project](https://github.com/jbusecke/cookiecutter-science-project) template written by [Julius Busecke](http://jbusecke.github.io/). The project is organized as an installable conda package.

To get setup, first pull the directory from github to your local machine:

``` bash
$ git clone https://github.com/edunnsigouin/l21
```

Then install the conda environment:

``` bash
$ conda env create -f environment.yml
```

Then install the project package:

``` bash
$ python setup.py develop
```

Finally change the project and data directories in l21/config.py to your local directories

Support
-------
This research was funded by Research Council of Norway grants Dynamite 255027, Nansen Legacy 276730, and visiting fellowship 287930. [Sigma2](https://www.sigma2.no/metacenter) is acknowledged for providing computing and storage facilities under project NS9625K.
