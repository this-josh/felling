# How logging :evergreen_tree: can up your python game

```python
print("Hello World!")
```

This is something we are all familiar with, the start of every *'Learn Python today!'* course uses it. `print` is great when initially writing some code, but suffers drawbacks when your code gets serious. When debugging code, you use a debugger not print statements, when running code you should use logs to see what is happening.

> Logging is the best way to understand what your code is doing

## Writing your first log

```python
import logging
logging.info("Hello World!")
```

What happens here? First, we must import logging a package bundled with python. In line 2 we log “Hello World” at log level *info*. If you run this, you’ll see “Hello World!" isn’t printed, this is down to our logging configuration.

## Why log instead of print?

Logging allows you to categorise messages based on their severity, for example, is this a warning? Is it only useful in debugging? Additionally, it allows you to capture metadata surrounding the log, such as the file name the log comes from, and the time the log was produce.

## Logging levels

There are *5* different log levels:

```python
logging.debug()
logging.info()
logging.warning()
logging.error()
logging.critical()
```

We can use these different log levels where appropriate and handle them differently. For example, we don’t need to write every functions output to the stdout, but it could be useful to have a record of our codes inner workings, here you could use `logging.debug`. How different log levels are handled is controlled by our logging configuration, a topic that will be discussed shortly.

While there are 5 log levels, there is a sixth useful logging method, `logging.exception`

```python
try:
	raise ValueError
except ValueError as e:
	logging.exception(e.args)
```

`logging.exception` should only be used in try and except statements, it logs an error message along with the exceptions traceback.

## Configuring logging

The power of logging comes from how you configure it. However, as you’d expect from such a flexible tool logging can be complex.

### Different loggers

It is typically advised to configure a logger for each file by doing the following:

```python
import logging
logger = logging.getLogger(__name__)
```

`logger` is now a logger which has the files name, making it easy to 

### Different handles

A handler is part of the logging config, it specifies how python should deal with a log level. For example, only write `warning` and `critical` logs to the stdout. Or write all logs `debug` and higher to the stdout for a specific package.

## Logging sounds interesting but configuring loggers sounds complicated

If this sounds like you, this is where my python package `felling` comes it. It is bundled with a json file which provides a better default config than `logging.basicConfig`

### Felling stdout

```
2021-03-18 19:50:55 - inout - INFO - Reading in file_to_read 
```

Above is a sample stdout from Felling there are 4 things to note here

1. 2021-03-18 19:50:55
   1. It displays the time of the log
2. inout
   1. It provides the name of the logger providing the log
3. INFO
   1. The log level
4. Reading in file_to_read 
   1. The log message

### Felling log file

Felling always saves logs to a file. By default it will create a `log` dir at root, and a file `{time_runtime_started}_{main_file_name}.log`

```
2021-03-18 19:50:55 - inout - INFO - inout.read_file - on line 8 - Reading in file_to_read - /why_logging/inout.py
```

As can be seen, the log file captures all the information that [Felling stdout](### Felling stdout), additionally it captures

1. inout.read_file
   1. The file name and the method name
2. on line 8
   1. The line in the file the log originates from
3. /why_logging/inout.py
   1. The absolute path to the file





Logging has numerous key advantages over print statements

* Different log levels help categorise what is going on, and handle the different levels appropriately
* Logs make it easy to capture metadata surrounding the log
* We can easily save logs to a file, this also gets around stdout overflow

