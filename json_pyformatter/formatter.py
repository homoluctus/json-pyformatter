import json
from collections import OrderedDict
from logging import Formatter


class JsonFormatter(Formatter):
    """
    Formatter outputs logging as JSON

    The supported fields are:

    name:       Name of the logger (logging channel)
    levelno:    Numeric logging level for the message
                (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    levelname:  Text logging level for the message
                ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
    pathname:   Full pathname of the source file where
                the logging call was issued
    filename:   Filename portion of pathname
    module:     Module (name portion of filename)
    lineno:     Source line number where the logging call was issued
    funcName:   Function name
    created:    Time when the LogRecord was created
                (time.time()return value)
    asctime:    Textual time when the LogRecord was created
    msecs:      Millisecond portion of the creation time
    relativeCreated:
                Time in milliseconds when the LogRecord was created,
                relative to the time the logging module was loaded
                (typically at application startup time)
    thread:     Thread ID
    threadName: Thread name
    process:    Process ID
    message:    The result of record.getMessage(),
                computed just as the record is emitted

    (In details, please refere to
    https://docs.python.org/3/library/logging.html#logrecord-attributes)
    """

    default_fields = ('asctime', 'levelname', 'message')

    def __init__(self, fields=None, datefmt=None, indent=None):
        """
        Args:
            fields (tuple, list)
            datefmt (str)
            indent (str, int)
        """

        self.fields = (
            self.get_or_none(fields, (list, tuple)) or self.default_fields
        )
        # default time format is %Y-%m-%d %H:%M:%S
        self.datefmt = (
            self.get_or_none(datefmt, str) or self.default_time_format
        )
        self._indent = self.get_or_none(indent, (str, int))

    def get_or_none(self, target, types):
        """Check whether target value is expected type.
        If target type does not match expected type, returns None.

        Args:
            target (any)
            types (class, tuple)

        Returns:
            target or None
        """

        if isinstance(target, types):
            return target
        return None

    def getMessage(self, record):
        if isinstance(record.msg, (list, tuple, dict)):
            return record.msg
        return record.getMessage()

    def _format_json(self, record):
        return json.dumps(record, ensure_ascii=False, indent=self._indent)

    def _format(self, record):
        log = OrderedDict()

        try:
            for field in self.fields:
                log[field] = getattr(record, field)
            return log
        except AttributeError as err:
            raise ValueError(f'Formatting field not found in log record {err}')

    def format(self, record):
        record.message = self.getMessage(record)
        record.asctime = self.formatTime(record, self.datefmt)
        formatted_record = self._format(record)
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            formatted_record['traceback'] = [
                msg.strip() for msg in record.exc_text.strip().split('\n')
            ]
        if record.stack_info:
            formatted_record['stack'] = record.stack_info.strip()

        return self._format_json(formatted_record)
