""" This file is used to add the parent directory to the sys.path
    so that the tests can import from the windtunnel."""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '..')))
