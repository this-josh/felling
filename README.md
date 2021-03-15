# felling :evergreen_tree:

>  **felling** *verb*: to cut down  
> 	Synonyms: Logging

[![PyPI Latest Release](https://img.shields.io/pypi/v/felling.svg)](https://pypi.org/project/felling/)[![License](https://img.shields.io/github/license/this-josh/felling)](https://github.com/this-josh/felling/blob/main/LICENSE)[![Python package](https://github.com/this-josh/felling/actions/workflows/python-package.yml/badge.svg?branch=main)](https://github.com/this-josh/felling/actions/workflows/python-package.yml)[![Coverage](https://codecov.io/github/this-josh/felling/coverage.svg?branch=main)](https://codecov.io/gh/this-josh/felling)[![Issues](https://img.shields.io/github/issues/this-josh/felling)](https://github.com/this-josh/felling/issues)[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/this-josh/felling.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/this-josh/felling/context:python)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


Felling easily improves repeatability and debugging of code by always initially logging some runtime metadata and ensuring logs are always written to a file in an easy to read format.

## Example usage

```python
import felling
felling.configure()
# Done!
```

## Issues

If you find any bugs/have any request, please feel free to add a GitHub ticket. It’s only through your ideas that felling can reach its full potential.

## Usage

1. Install the package with `pip install felling`

2. The package only needs to be imported once per runtime, in ```__main__``` run the following code  
    ```python
    import felling
    felling.configure()
    ```
    Logs will saved in `./logs/{time_ran}_{file_name}.log` where file_name will be the name of the file ```__main__``` unless a file_name is passed into ```felling.configure```
    At this point your logs are now configured for this run time and you can log as normal.


## Logging in Python :snake:

This is a basic explanation of logging in python, none of this is specific to felling.

First, you must import logging and name your logger, this is usually done by:  


```python
import logging
logger = logging.getLogger(__name__)
```

Now you can write logs, there are a few different levels which you can use. They are, in ascending order of severity:
   ```python
   logger.debug('lowest level')
   logger.info(message)
   logger.warning(message)
   logger.error(message)
   logger.critical(message)
   ```
   If you wish for execution information to be put into the log it can be done by:
   ```python
   logger.error('Everything has failed', exc_info = True)
   ```

Try and excepts can also be handled properly, for example:
```python
try:
    float('this cannot be a float') 
except ValueError as e:
    logger.exception('your message here')
    raise
except Exception as e:
    logger.exception(e.args)
    raise
```
*Line 3* `logger.exception('your message here')` will log your message, the error message and its full traceback. 

*Line 6* will then catch all other exceptions and log them, *Note* catching specific error is generally preferred.

### Testing
When running tests logging can be easily turned off if desired. In the file `tests/__init__.py` write:
```python
logging.disable()
```
By default this disables all logs of level critical and lower, felling is capable of reading this status and won't generate any empty log files. 

# Now go and write some beautiful logs :sunrise_over_mountains:

## felling additional features

`felling.configure()` has a lot more features than outlined in the basic summary above, they can be seen below

### Initial logs

For repeatability it can be useful to have some metadata about each run time. When configuring felling it will log:

1. The users username
2. The most recent git commit hash for `__main__`'s repo, its fine if it isn’t a git repo.
3. The git remote status from `git remote show origin`

### `log_path`

```python
import felling
felling.configure(log_path = './logs')
```

When configuring a `pathlib.Path` or a `str` path can be provide as the directory to save logs to, if none is provided `'./logs'` will be used

### `log_file_name`

```python
import felling
felling.configure(log_file_name = 'logs_for_foo')
```

When configuring, a custom log file name can be passed

### `file_log_level` and `std_log_level`

```python
import felling
felling.configure(file_log_level ='ERROR', std_out_log_level = 40)
```

Log levels can be provided either as a string (`“ERROR”`) or integer (`40`) as defined [here](https://docs.python.org/3/library/logging.html#logging-levels). `file_log_level` defines the minimum log level which will be written to the log file, while `std_out_log_level` defines the minimum log level which will be written to the std output (your terminal)

### `error_only_modules`

```python
import felling
import pandas
felling.configure(error_only_modules = pandas)
```

If some packages are writing lots of logs you’re not interested in a specific error_only handler can be set up. In the above example only pandas error logs will be used. Some packages have control for their verbosity of logging, however, setting it up with felling works for all packages and is comprehensive. 

### `modules_to_debug`

```python
import felling
import pandas
felling.configure(modules_to_debug = pandas)
```

Similar to [error_only_modules](## `error_only_modules`) you can specify modules which you would like debug logs to be interpreted

### `package_versions_to_log`


```python
import felling
import pandas
felling.configure(package_versions_to_log = pandas)
```

For repeatability it can be helpful to log package versions, packages passed to `package_versions_to_log` will have their version numbers logged while running initial logs

### Comparing log files

Have you refactored some code? Do you not have 100% test coverage? Of course not “it’s only experimental code” :wink: We all know what you have done. We can compare before and after log files to add some extra validity to your code change or to easily find where things change

*Note:  This is **absolutely** not a replacement to testing, and will only provide any benefit if you have comprehensive debug logs* 

#### How to run

The following script will run the comparison.

```shell
python -m felling {str_to_first_log_file} {str_to_second_log_file} [-v]
```

If all is identical it’ll let you know, otherwise it will print the first 100 differences. If you’d like more than 100 differences pass `-v`

## Isn’t felling a bit simple?

> Simple is better than complex.

​	*`python -c import this ` - Tim Peters*

Wherever possible `felling` will be kept as simple as possible, for now I am proud it is requirements free. A lot of the difficulty in setting this up has been gathering an understanding of logging in Python and the initial setup of logging.json. 


## Other advantages:
*   If you have too many print statement you'll lose them in your stdout but still have them in a log file