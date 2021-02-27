# felling

This packages uses a json file to configure your logging parameters making logging simpler and easily consistent.

## Usage

1. Install the package with ```python setup.py install```
2. The package only needs to be imported once per runtime, in ```__main__``` run the following code  
    ```
    log_path = Path('place_where_you_want_logs')
    from felling import felling
    felling.configure_logger(log_path=log_path)
    ``` 
    Logs will saved in the specified log_path as ```{time_ran}_{file_name}_info.log``` where file_name will be the name of the file ```__main__``` unless a file_name is passed into ```felling.configure_logger```
    At this point your logs are now configured for this run time and you can log as normal.

## Normal logging in Python :snake:
First, you must import logging and name your logger, this is usually done by:  

    
    import logging
    logger = logging.getLogger(__name__)
    


Now you can write logs, there are a few different levels you can do:
   ```
   logger.debug('lowest level')
   logger.info(message)
   logger.warning(message)
   logger.error(message)
   logger.critical(message)
   ```
   If you wish for execution information to be put into the log it can be done by:
   ```
   logger.error('Everything has failed', exc_info = True)
   ```
   In the felling json file (_logger.json_) different handlers are defined for different log levels. For example, by default all logs will be printed to console, whereas only info and higher will be saved to the info file.


Try and excepts can also be handled properly, for example:
```
try:
    float('this cannot be a float') 
except: ValueError as e:
    logger.exception(('your message can go here', e))
```
Note that exceptions must be provided for individual error types, or Exception can be used to catch all errors.  
By using ```logger.exception()``` the full error message traceback will also be logged.

### Testing
When running tests logging can be easily turned off. In the file _tests/\_\_init\_\_.py_ write:
```
logging.disable()
```
By default this disables all logs of level critical and lower which unless specific levels are being used will mean all logs are disabled.
felling is capable of reading this status and won't generate any empty log files

# Now go and write some beautiful logs :sunrise_over_mountains:


## felling additional features (advanced usage)
:exclamation: __Important__: While changing the file _logger.json_ allows for easy customisation it may result in your logs differing from your colleagues.


If you do wish to modify the _logger.json_ file you should install felling with ```python setup.py develop```  

### Problematic package
If particular package is causing problems a custom handler can be defined in _logger.json_, and example can be seen under the keys _loggers_>_specific module_. Here you can make a handler for problematic package which writes even debug logs to a log file.

### Changing current handlers


Within the _logger.json_ file the current loggers can be changed. Here you may want only critical error messages to be printed to the console, or you may want to change the log file formatting for example. 



## TODO:
*   It would be better if custom configurations could be passed to  ```felling.configure_logger``` rather than having to modify the json file.