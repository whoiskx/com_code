# -*-coding:utf-8-*-

import time
from logging import FileHandler, Handler, ERROR, Formatter

from comm.log.loghub_helper import Producer

try:
    import codecs
except ImportError:
    codecs = None


class DailyRotatingHandler(FileHandler):
    def __init__(self, filename, max_bytes, mode='a', encoding='utf-8'):
        if codecs is None:
            encoding = None
        FileHandler.__init__(self, filename, mode, encoding, delay=1)
        self.fn_prefix = self.baseFilename
        self.st = None
        self.max_bytes = max_bytes

    def _open_file(self):
        self.st = time.localtime()
        suffix = time.strftime('%Y-%m-%d', self.st)
        self.baseFilename = '%s.%s' % (self.fn_prefix, suffix)
        return self._open()

    def should_skip(self, record):
        if self.stream is None:
            self.stream = self._open_file()

        if self.max_bytes > 0:
            msg = "%s\n" % self.format(record)
            self.stream.seek(0, 2)
            if self.stream.tell() + len(msg) >= self.max_bytes:
                return 1
        return 0

    def should_rollover(self, record):
        if self.stream is None:
            self.stream = self._open_file()

        st = time.localtime()
        if st.tm_mday != self.st.tm_mday or st.tm_mon != self.st.tm_mon or st.tm_year != self.st.tm_year:
            return 1
        return 0

    def do_rollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        self.stream = self._open_file()

    def emit(self, record):
        try:
            if self.should_rollover(record):
                self.do_rollover()
            if self.should_skip(record):
                return
            FileHandler.emit(self, record)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


class LoghubFormatter(Formatter):
    from logging import LogRecord
    DEFAULT_PROPERTIES = LogRecord(
        '', '', '', '', '', '', '', '').__dict__.keys()

    def format(self, record):
        """Formats LogRecord into python dictionary."""
        # Standard document
        document = {
            'level': record.levelname,
            'thread': record.thread,
            'threadName': record.threadName,
            'message': record.getMessage(),
            'loggerName': record.name,
            'fileName': record.pathname,
            'module': record.module,
            'method': record.funcName,
            'lineNumber': record.lineno
        }

        if record.exc_info is not None:
            document.update({
                'exception': {
                    'message': str(record.exc_info[1]),
                    'code': 0,
                    'stackTrace': self.formatException(record.exc_info)
                }
            })

        if len(self.DEFAULT_PROPERTIES) != len(record.__dict__):
            contextual_extra = set(record.__dict__).difference(
                set(self.DEFAULT_PROPERTIES))
            if contextual_extra:
                for key in contextual_extra:
                    document[key] = record.__dict__[key]
        return document


class LogHubHandler(Handler):
    def __init__(self, level=ERROR, fail_silently=True):
        Handler.__init__(self, level)
        self.producer = Producer()
        self.fail_silently = fail_silently
        self.formatter = LoghubFormatter()

    def emit(self, record):
        """Send error record to loghub."""
        try:
            self.send(self.format(record))
        except Exception as e:
            if not self.fail_silently:
                self.handleError(record)
            else:
                print e

    def __exit__(self, type, value, traceback):
        pass

    def send(self, error_msg):
        self.producer.send("error", error_msg)


class BufferedLogHubHandler(LogHubHandler):
    pass


if __name__ == "__main__":
    import logging

    logger = logging.getLogger(__name__)
    logger.addHandler(DailyRotatingHandler('/home/kiwi/tmp/pylog', 1024))
    logger.debug('sdfjksdflksdjflksd')
    for i in xrange(1000):
        logger.error('erorewewj ew')
