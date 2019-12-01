# json-pyformatter

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/homoluctus/json-pyformatter/Test)
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/homoluctus/json-pyformatter?include_prereleases)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/json-pyformatter)
![GitHub](https://img.shields.io/github/license/homoluctus/json-pyformatter)

Python logging outputs as JSON.<br>
This JsonFormatter is written in Pure Python.

## Installation

```bash
pip install json-pyformatter
```

## Usage

```python
import logging
from json_pyformmatter import JsonFormatter

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
fields = ('levelname', 'filename', 'message')
handler.setFormatter(JsonFormatter(fields=fields))
logger.addHandler(hander)

logger.info('hello')
```

default fields is ('asctime', 'levelname', 'message')<br>
Other supported fields are:

|field name|description|
|:--:|:--|
|name|Name of the logger (logging channel)|
|levelno|Numeric logging level for the message<br>(DEBUG, INFO, WARNING, ERROR, CRITICAL)|
|levelname|Text logging level for the message<br>("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")|
|pathname|Full pathname of the source file where the logging call was issued|
|filename|Filename portion of pathname|
|module|Module (name portion of filename)|
|lineno|Source line number where the logging call was issued|
|funcName|Function name|
|created|Time when the LogRecord was created (time.time()return value)|
|asctime|Textual time when the LogRecord was created|
|msecs|Millisecond portion of the creation time|
|relativeCreated|Time in milliseconds when the LogRecord was created, relative to the time the logging module was loaded (typically at application startup time)|
|thread|Thread ID|
|threadName|Thread name|
|process|Process ID|
|message|The result of record.getMessage(), computed just as the record is emitted|

In details, please refere to [logrecord-attributes](https://docs.python.org/3/library/logging.html#logrecord-attributes)

## Output

```bash
{"levelname": "INFO", "filename": "test_formatter.py", "message": "hello"}
```

If specify indent option as 2, the result is as follows:

```bash
{
  "levelname": "INFO",
  "filename": "test_formatter.py",
  "message": "hello"
}
```

When exc_info is True, the result includes traceback infomation as follows:

```bash
{
  'asctime': '2019-12-01 13:58:34',
  'levelname': 'ERROR',
  'message': 'error occurred !!',
  'traceback': [
    'Traceback (most rec...ll last):',
    'File "/example/test..._exc_info',
    'raise TypeError(message)',
    'TypeError: error occurred !!'
  ]
}
```

Logging message type is dict:

```bash
{
  'asctime': '2019-12-01 23:34:32',
  'levelname': 'INFO',
  'message': {
    'id': '001',
    'msg': 'This is test.',
    'name': 'test'
  }
}
```
