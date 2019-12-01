import json
import logging
import pytest
import filecmp
from pathlib import Path

# from collections import OrderedDict
from json_pyformatter.formatter import JsonFormatter


@pytest.fixture()
def logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    return logger


class TestJsonFormatter:
    def test_default_fields(self, caplog, logger):
        formatter = JsonFormatter()
        logger.handlers[0].setFormatter(formatter)

        message = 'hello'
        logger.info(message)
        result = json.loads(caplog.text)
        assert result['message'] == message
        assert result['levelname'] == 'INFO'
        assert tuple(result.keys()) == formatter.default_fields

    def test_custom_fields(self, caplog, logger):
        custom_fields = (
            'asctime',
            'levelname',
            'module',
            'filename',
            'lineno',
            'message',
        )
        formatter = JsonFormatter(custom_fields)
        logger.handlers[0].setFormatter(formatter)

        message = 'hello'
        logger.info(message)
        result = json.loads(caplog.text)
        assert result['message'] == message
        assert result['levelname'] == 'INFO'
        assert result['filename'] == Path(__file__).name
        assert tuple(result.keys()) == custom_fields

    def test_invalid_field(self, capsys, logger):
        custom_fields = (
            'this is invalid field',
            'asctime',
            'levelname',
            'module',
            'filename',
            'lineno',
            'message',
        )
        formatter = JsonFormatter(custom_fields)
        logger.handlers[0].setFormatter(formatter)

        message = 'faild'
        logger.info(message)
        result = capsys.readouterr().err
        assert 'ValueError' in result

    def test_logger_warn(self, caplog, logger):
        formatter = JsonFormatter()
        logger.handlers[0].setFormatter(formatter)
        message = 'error occurred !!'

        try:
            raise TypeError(message)
        except TypeError as err:
            logger.warn(err)

        result = json.loads(caplog.text)
        assert result['message'] == message
        assert result['levelname'] == 'WARNING'
        assert tuple(result.keys()) == formatter.default_fields

    def test_logger_warn_with_stack_info(self, caplog, logger):
        formatter = JsonFormatter()
        logger.handlers[0].setFormatter(formatter)
        message = 'error occurred !!'

        try:
            raise TypeError(message)
        except TypeError as err:
            logger.warn(err, stack_info=True)

        result = json.loads(caplog.text)
        expected_fields = ('asctime', 'levelname', 'message', 'stack')
        assert result['message'] == message
        assert result['levelname'] == 'WARNING'
        assert tuple(result.keys()) == expected_fields

    def test_logger_error(self, caplog, logger):
        formatter = JsonFormatter()
        logger.handlers[0].setFormatter(formatter)
        message = 'error occurred !!'

        try:
            raise TypeError(message)
        except TypeError as err:
            logger.error(err)

        result = json.loads(caplog.text)
        assert result['message'] == message
        assert result['levelname'] == 'ERROR'
        assert tuple(result.keys()) == formatter.default_fields

    def test_logger_error_with_exc_info(self, caplog, logger):
        formatter = JsonFormatter()
        logger.handlers[0].setFormatter(formatter)
        message = 'error occurred !!'

        try:
            raise TypeError(message)
        except TypeError as err:
            logger.error(err, exc_info=True)

        result = json.loads(caplog.text)
        expected_fields = ('asctime', 'levelname', 'message', 'traceback')
        assert result['message'] == message
        assert result['levelname'] == 'ERROR'
        assert tuple(result.keys()) == expected_fields

    def test_logger_exception(self, caplog, logger):
        formatter = JsonFormatter()
        logger.handlers[0].setFormatter(formatter)
        message = 'error occurred !!'

        try:
            raise TypeError(message)
        except TypeError as err:
            logger.exception(err)

        result = json.loads(caplog.text)
        expected_fields = ('asctime', 'levelname', 'message', 'traceback')
        assert result['message'] == message
        assert result['levelname'] == 'ERROR'
        assert tuple(result.keys()) == expected_fields

    def test_logger_critical(self, caplog, logger):
        formatter = JsonFormatter()
        logger.handlers[0].setFormatter(formatter)
        message = 'error occurred !!'

        try:
            raise TypeError(message)
        except TypeError as err:
            logger.critical(err)

        result = json.loads(caplog.text)
        assert result['message'] == message
        assert result['levelname'] == 'CRITICAL'
        assert tuple(result.keys()) == formatter.default_fields

    def test_indent(self, caplog, logger):
        indent = 2
        fields = ('levelname', 'filename', 'message')
        formatter = JsonFormatter(fields=fields, indent=indent)
        logger.handlers[0].setFormatter(formatter)

        message = 'hello'
        logger.info(message)
        result_file = 'tests/caplog.json'
        with open(result_file, 'w') as fd:
            fd.write(caplog.text.strip())

        assert (
            filecmp.cmp('tests/test.json', result_file, shallow=False) is True
        )

        Path(result_file).unlink()

    def test_message_as_dict(self, caplog, logger):
        logger.handlers[0].setFormatter(JsonFormatter())

        message = {'id': '001', 'name': 'test', 'msg': 'This is test.'}
        logger.info(message)
        result = json.loads(caplog.text)

        assert result['message'] == message
        assert isinstance(result['message'], dict) is True
        assert tuple(result.keys()) == JsonFormatter.default_fields
