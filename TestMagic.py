#!/usr/bin/env python3

# pylint: disable = bad-whitespace
# pylint: disable = invalid-name
# pylint: disable = missing-docstring
# pylint: disable = global-statement

# https://docs.python.org/3.4/reference/simple_stmts.html#grammar-token-assert_stmt

# -------
# imports
# -------

from io import StringIO
from unittest import main, TestCase

from models import Card, Artist
# -----------
# TestMagic
# -----------


class TestMagic (TestCase):

    # ----
    # CARD
    # ----

    def test_card_1(self):
        self.assertEqual(0, 0)

# ----
# main
# ----

if __name__ == "__main__":  # pragma: no cover
    main()
