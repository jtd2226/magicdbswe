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
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from testmodels import app, db, MCard, MSet, MArtist, MSubtype

# -----------
# TestMagic
# -----------

class TestMagic (TestCase):


    def create_app(self):
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
    # ----
    # CARD
    # ----

    def test_card_1(self):

        db.session.commit()
        db.drop_all()
        db.create_all()

        example3 = MSubtype("gobbo", 2)
        db.session.add(example3)
        db.session.commit()

        example1 = MCard("123", "name", "Creature", [example3], "flying", 'ktk', 5, "Red", 1, 1, "url", "common", "thomas")
        db.session.add(example1)
        db.session.commit()

        card = db.session.query(MCard).filter_by(name="name").first()
        self.assertEqual(card.name, "name")
        self.assertEqual(card.mainType, "Creature")

        db.session.commit()
        db.drop_all()

    def test_card_2(self):

        db.session.commit()
        db.drop_all()
        db.create_all()

        example3 = MSubtype("gobbo", 2)
        db.session.add(example3)
        db.session.commit()

        example1 = MCard("123", "name", "Creature", [example3], "flying", 'ktk', 5, "Red", 1, 1, "url", "common", "thomas")
        db.session.add(example1)
        db.session.commit()

        card = db.session.query(MCard).filter_by(name="name").first()
        self.assertEqual(card.expansionSet, "ktk")
        self.assertEqual(card.text, "flying")

        db.session.commit()
        db.drop_all()

    def test_card_3(self):

        db.session.commit()
        db.drop_all()
        db.create_all()

        example3 = MSubtype("gobbo", 2)
        db.session.add(example3)
        db.session.commit()

        example1 = MCard("123", "name", "Creature", [example3], "flying", 'ktk', 5, "Red", 1, 1, "url", "common", "thomas")
        db.session.add(example1)
        db.session.commit()

        card = db.session.query(MCard).filter_by(name="name").first()
        self.assertEqual(card.power, '1')
        self.assertEqual(card.toughness, '1')

        db.session.commit()
        db.drop_all()

    def test_relations(self):

        db.session.commit()
        db.drop_all()
        db.create_all()

        example3 = MSubtype("gobbo", 2)
        db.session.add(example3)
        db.session.commit()

        example1 = MCard("123", "name", "Creature", [example3], "flying", 'ktk', 5, "Red", 1, 1, "url", "common", "thomas")
        db.session.add(example1)
        db.session.commit()

        example2 = MCard("124", "weewoocardnumber2", "Creature", [example3], "flying", 'ktk', 5, "Red", 1, 1, "url", "common", "thomas")
        db.session.add(example2)
        db.session.commit()

        exampleSet = MSet('ktk', "Khans of Tarkir", "1", "none", 5, "link", [example3])
        db.session.add(exampleSet)
        db.session.commit()

        eset = db.session.query(MSet).filter_by(code='ktk').first()
        self.assertEqual(len(eset.cards.all()), 2)

        db.session.commit()
        db.drop_all()

    def test_many_relations(self):

        db.session.commit()
        db.drop_all()
        db.create_all()

        example3 = MSubtype("gobbo", 2)
        db.session.add(example3)
        db.session.commit()

        exampleSet = MSet('ktk', "Khans of Tarkir", "1", "none", 5, "link", [example3])
        db.session.add(exampleSet)
        db.session.commit()

        example1 = MCard("123", "name", "Creature", [example3], "flying", 'LEA', 5, "Red", 1, 1, "url", "common", "thomas")
        db.session.add(example1)
        db.session.commit()

        example2 = MCard("124", "weewoocardnumber2", "Creature", [example3], "flying", 'ktk', 5, "Red", 1, 1, "url", "common", "thomas")
        db.session.add(example2)
        db.session.commit()

        est = db.session.query(MSubtype).filter_by(name="gobbo").first()
        self.assertEqual(len(est.xcards.all()), 2)

        db.session.commit()
        db.drop_all()


    def test_many_relations2(self):

        db.session.commit()
        db.drop_all()
        db.create_all()

        example3 = MSubtype("gobbo", 2)
        db.session.add(example3)
        db.session.commit()

        exampleSet = MSet('ktk', "Khans of Tarkir", "1", "none", 5, "link", [example3])
        db.session.add(exampleSet)
        db.session.commit()

        exampleSet2 = MSet('LEA', "Khans of Tarkir", "1", "none", 5, "link", [example3])
        db.session.add(exampleSet2)
        db.session.commit()

        est = db.session.query(MSubtype).filter_by(name="gobbo").first()
        self.assertEqual(len(est.ssets.all()), 2)

        db.session.commit()
        db.drop_all()

    def test_many_relations3(self):

        db.session.commit()
        db.drop_all()
        db.create_all()

        example3 = MSubtype("gobbo", 2)
        db.session.add(example3)
        db.session.commit()

        exampleSet = MSet('ktk', "Khans of Tarkir", "1", "none", 5, "link", [example3])
        db.session.add(exampleSet)
        db.session.commit()

        example1 = MArtist('Thomas', 5, 5, [exampleSet])
        db.session.add(example1)
        db.session.commit()

        example2 = MArtist('Thom', 5, 5, [exampleSet])
        db.session.add(example2)
        db.session.commit()

        est = db.session.query(MSet).filter_by(code="ktk").first()
        self.assertEqual(len(est.xartists.all()), 2)

        db.session.commit()
        db.drop_all()

    def test_set_1(self):
        db.session.commit()
        db.drop_all()
        db.create_all()

        example3 = MSubtype("gobbo", 2)
        db.session.add(example3)
        db.session.commit()

        exampleSet = MSet('MM3', "Modern Masters 2017 Edition", "1", "none", 5, "link", [example3])
        db.session.add(exampleSet)
        db.session.commit()

        est = db.session.query(MSet).filter_by(code="MM3").first()
        self.assertEqual(est.code, 'MM3')
        db.session.commit()
        db.drop_all()

    def test_set_2(self):
        db.session.commit()
        db.drop_all()
        db.create_all()

        example3 = MSubtype("gobbo", 2)
        db.session.add(example3)
        db.session.commit()

        exampleSet = MSet('KLD', "Kaladesh", "1", "none", 5, "link", [example3])
        db.session.add(exampleSet)
        db.session.commit()

        est = db.session.query(MSet).filter_by(code="KLD").first()
        self.assertEqual(est.name, 'Kaladesh')
        db.session.commit()
        db.drop_all()

    def test_set_3(self):
        db.session.commit()
        db.drop_all()
        db.create_all()

        example3 = MSubtype("gobbo", 2)
        db.session.add(example3)
        db.session.commit()

        exampleSet = MSet('LEA', "Limited Edition Alpha", "1", "none", 5, "link", [example3])
        db.session.add(exampleSet)
        db.session.commit()

        est = db.session.query(MSet).filter_by(code="LEA").first()
        self.assertEqual(est.name, "Limited Edition Alpha")
        db.session.commit()
        db.drop_all()

# ----
# main
# ----

if __name__ == "__main__":  # pragma: no cover
    main()
