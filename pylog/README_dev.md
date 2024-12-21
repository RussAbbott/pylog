## Dev Environment Setup

1. `cd` to the current directory
2. run `pip install -e .[dev,test]`. The parameter `-e` will install the package as an [editable install](https://pip.pypa.io/en/stable/topics/local-project-installs/), so that changes to the source files will be immediately available to other users of the package on our system.  You can run `pip install -e .` without the `[dev,test]` if you are reinstalling, and don't need the test or development dependancies. 
3. Use it in examples/tests by importing modules from `pylog` package
4. To Build the Python Packgae, run `python -m build`.
5. Keep a .devx suffix on the release number in pyroject.toml until you are absolutely ready to release.  
6. To release, remove the .devx suffix, and use the github ation to create a release.  That will push the release up to PyPi.  You can publish a pre-release the same way,
just leave the .devx suffix on the version number;  in that case you can install the prerelease with `pip install --pre pylog`.  

## About Tests

1. `cd` to the current directory.
2. run `pytest`. This will invoke `pytest` which will find and run all the tests placed inside `tests\` directory.  [pyrojrect.toml](pyproject.toml) contains the pytest command line arguments in `[tool.pytest.ini_options]`.  
3. Group tests by putting them inside the relevent directories e.g. put unit tests in `tests\pylog\unit\`
4. Follow the standard convention for test assets i.e. naming each file as `test_{python_module}.py` e.g. `test_logic_variables.py`
    * These are the default test discovery rules that `pytest` follows:
    > 1. If no arguments are specified then collection starts from testpaths (specified in [pyrojrect.toml](pyproject.toml)) or the current directory. Alternatively, command line arguments can be used in any combination of directories, file names or node ids.
    > 2. Recurse into directories, unless they match norecursedirs.
    > 3. In those directories, search for test_*.py or *_test.py files, imported by their test package name.
    > 4. From those files, collect test items:
    >     * test prefixed test functions or methods outside of class
    >     * test prefixed test functions or methods inside Test prefixed test classes (without an __init__ method)
    
5. It is recommended to maintain the same directory structure in `pylog\unit\` as it is in `src\pylog`
## TODO: Other project details
