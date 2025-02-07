import unittest


def suite():
    return unittest.TestLoader().discover("portfolio.tests", pattern="*.py")
