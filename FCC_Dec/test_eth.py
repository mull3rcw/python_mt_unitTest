#!/usr/bin/python

import socket               # Import socket module



#!/usr/bin/env python
#
# Large numbers of unit tests
# 
# $Id: manytests.py,v 1.2 2001/08/06 09:10:00 purcell Exp $

import unittest

class TestCase(unittest.TestCase):
	s = socket.socket()         # Create a socket object
	host = socket.gethostname() # Get local machine name
	print host
	port = 5000                # According to John Chang

	s.connect((host, port))
	print s.recv(1024)
	s.close                     # Close the socket when done

def suite():
    return unittest.makeSuite(TestCase)


if __name__ == '__main__':
    # When this module is executed from the command-line, run all its tests
    unittest.TextTestRunner().run(suite())