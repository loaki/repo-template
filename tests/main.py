import logging
import sys
import unittest

from xmlrunner import XMLTestRunner


def run() -> None:
    loader = unittest.TestLoader()
    tests = loader.discover(".")
    test_runner = XMLTestRunner(verbosity=2, output="reports/tests")
    logging.disable()
    ret = not test_runner.run(tests).wasSuccessful()
    sys.exit(ret)


if __name__ == "__main__":
    run()
