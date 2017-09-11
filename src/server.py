#!/usr/local/bin/python
# coding: utf8

'''
    File name: server.py
    File description: Serves search functionality
    Author: Umesh Singla
    Date created: Aug 21, 2017
    Python Version: 2.7
'''

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from urlparse import urlparse, parse_qs
from search import search

import sys

class SearchServer(BaseHTTPRequestHandler):
    """
    """
    def do_HEAD(self):
        """
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        """
        """
        self.do_HEAD()

        _GET = parse_qs(urlparse(self.path).query)

        if 'q' in _GET:
            query = _GET['q'][0]
            terms = query.strip().lower().split()
            result = search.search(terms)

            self.wfile.write("<html><head><title>Search result</title></head>")
            self.wfile.write("<body>")
            self.wfile.write("<p style='color:#fab'>Result in "+str(result['time'])+" seconds</p>")
            for page in result['pages']:
                self.wfile.write("<p>"+page[1]+"</p>")
            self.wfile.write("<p style='color:#fab'>You accessed path: %s</p>" % self.path)
            self.wfile.write("</body></html>")

        self.finish()


def start(indexDir):
    """
    """
    search.initialize(indexDir)
    try:
        server_address = ('', 8000)
        httpd = HTTPServer(server_address, SearchServer)
        print "Serving on http://localhost:8000 ..."
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\rShutting down...')
        httpd.socket.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: python server.py <indexDir>\n")
        exit(1)
    start(sys.argv[1])