import json
from collections import OrderedDict
from logging import Formatter


class JsonFormatter(Formatter):
    default_fields = ('asctime', 'levelname', 'message')

    def __init__(self, fields=None, datefmt=None, indent=None):
        """
        Args:
            fields (tuple, list)
            datefmt (str)
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

    def _format_json(self, record):
        return json.dumps(record, ensure_ascii=False, indent=self._indent)

    def _format(self, record):
        try:
            log = OrderedDict()
            for field in self.fields:
                log[field] = getattr(record, field)
            return log
        except AttributeError as err:
            raise ValueError(f'Formatting field not found in log record {err}')

    def format(self, record):
        record.message = record.getMessage()
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
