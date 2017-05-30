import unittest
from pathlib import Path

from webserver.web_server import WebServer

class TestWebServer(unittest.TestCase):
    def test_start(self):
        server = WebServer(Path('../data'))
        server.start()  # todo: causes infinite loop


if __name__ == '__main__':
    unittest.main()
