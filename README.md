# felling :evergreen_tree:

>  **felling** *verb*: to cut down  
> 	Synonyms: Logging

Felling easily improves repeatability and debugging of code by always initially logging some runtime metadata and ensuring logs are always written to a file

```python
import felling
felling.configure()
# Done!
```
[TOC]

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

This is a basic explanation of logging in python, none of this is specific too felling.

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
2. The most recent git commit hash for `__main__`s repo, its fine if it isn’t a git repo.
3. The git remote status from `git remote show origin`

### `log_path`

```python
import felling
felling.configure(log_path = './logs')
```

When configuring a `pathlib.Path` or a `str` path can be provide as the directory to save logs to.

### `log_file_name`

```python
import felling
felling.configure(log_file_name = 'logs_for_foo')
```

When configuring a custom file name for the log file can be passed

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

For repeatability it can be helpful to log package versions, packages past to `package_versions_to_log` will have their version numbers logged while running initial logs