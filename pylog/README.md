## Dev Environment Setup

1. `cd` to the current directory
2. run `pip install -e .`. The parameter `-e` will install the package with a symlink, so that changes to the source files will be immediately available to other users of the package on our system.
3. Use it in examples/tests by importing modules from `pylog` package

## About Tests

1. `cd` to the current directory
2. run `python setup.py test`. This will invoke `pytest` which will find and run all the tests placed inside `tests\` directory
3. Group tests by putting them inside the relevent directories e.g. put unit tests in `tests\unit\`
4. Follow the standard convention for test assets i.e. naming each file as `test_{python_module}.py` e.g. `test_logic_variables.py`
    * These are the default test discovery rules that `pytest` follows:
    > 1. If no arguments are specified then collection starts from testpaths (if configured) or the current directory. Alternatively, command line arguments can be used in any combination of directories, file names or node ids.
    > 2. Recurse into directories, unless they match norecursedirs.
    > 3. In those directories, search for test_*.py or *_test.py files, imported by their test package name.
    > 4. From those files, collect test items:
    >     * test prefixed test functions or methods outside of class
    >     * test prefixed test functions or methods inside Test prefixed test classes (without an __init__ method)
    
5. It is recommended to maintain the same directory structure in `unit\` as it is in `src\pylog`
## TODO: Other project details
