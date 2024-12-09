## How to use repository
* Install `pytest`: `pip install pytest` / `conda install pytest`
* Install `pylog` package:
  ```sh
  pip install -e pylog/.
  ```
* Run examples' tests:
  ```sh
  pytest examples/
  ```


## Abstract (from [WI 2020](http://wi2020.vcrab.com.au/) paper)

We examine the history of Artificial Intelligence, from its audacious beginnings to the current day. We argue that constraint programming (a) is the rightful heir and modern-day descendent of that early work and (b) offers a more stable and reliable platform for AI than deep machine learning.

We offer a tutorial on constraint programming solvers that should be accessible to most software developers. We show how constraint programming works, how to implement constraint programming in Python, and how to integrate a Python constraint-programming solver with other Python code. 


To install from [PyPi](https://pypi.org/project/pylog/): `pip install pylog``

If you are editing pylog source, running tests, or building installable packages for upload to [PyPi](https://pypi.org/project/pylog/), install as an editable install with test and buid prequisites:

  `pip install -e .[test,build]` from the project root directory.  If you don't want to run tests or build an installable package, 
  `pip install -e .`

  To build the installable package for upload:
  `py -m build` from the project root.

  To run the tests, run them from the project root:
  `pytest`


