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

        example1 = MCard(123, "name", "Creature", [example3], "flying", 'ktk', 5, "Red", 1, 1, "url", "common", "thomas")
        db.session.add(example1)
        db.session.commit()

        card = db.session.query(MCard).filter_by(name="name").first()
        self.assertEqual(card.name, "name")
        self.assertEqual(card.mainType, "Creature")

        db.session.commit()
        db.drop_all()

    def test_relations(self):

        db.session.commit()
        db.drop_all()
        db.create_all()

        example3 = MSubtype("gobbo", 2)
        db.session.add(example3)
        db.session.commit()

        example1 = MCard(123, "name", "Creature", [example3], "flying", 'ktk', 5, "Red", 1, 1, "url", "common", "thomas")
        db.session.add(example1)
        db.session.commit()

        example2 = MCard(124, "weewoocardnumber2", "Creature", [example3], "flying", 'ktk', 5, "Red", 1, 1, "url", "common", "thomas")
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

        example1 = MCard(123, "name", "Creature", [example3], "flying", 'LEA', 5, "Red", 1, 1, "url", "common", "thomas")
        db.session.add(example1)
        db.session.commit()

        example2 = MCard(124, "weewoocardnumber2", "Creature", [example3], "flying", 'ktk', 5, "Red", 1, 1, "url", "common", "thomas")
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



    #added subtypes to set
    #added sets to artist 

    # def test_card_2(self):
    #     with app.test_request_context():
    #         example1 = Card("name", "Creature", "Angel", "shine",
    #                            "Ham", 5, "Red", "pt", "url", "common", "thomas")

    #         db.session.add(example1)
    #         db.session.commit()

    #         card = db.session.query(Company).filter_by(name="name").first()
    #         self.assertEqual(card.SubType, "Angel")
    #         self.assertEqual(card.text, "shine")

    #         db.session.delete(example1)
    #         db.session.commit()

    # def test_card_3(self):
    #     with app.test_request_context():
    #         example1 = Card("name", "Creature", "Angel", "shine",
    #                            "Ham", 5, "Red", "pt", "url", "common", "thomas")

    #         db.session.add(example1)
    #         db.session.commit()

    #         card = db.session.query(Company).filter_by(name="name").first()
    #         self.assertEqual(card.color, "Red")
    #         self.assertEqual(card.pt, "pt")

    #         db.session.delete(example1)
    #         db.session.commit()

    # def test_set_1(self):
    #     with app.test_request_context():
    #         example1 = Set("name", "date", "block", "card",
    #                            5,"promo", "artist" )

    #         db.session.add(example1)
    #         db.session.commit()

    #         setz = db.session.query(Company).filter_by(name="name").first()
    #         self.assertEqual(setz.name, "name")
    #         self.assertEqual(setz.block, "block")

    #         db.session.delete(example1)
    #         db.session.commit()

    # def test_set_2(self):
    #     with app.test_request_context():
    #         example1 = Set("name", "date", "block", "card",
    #                            5,"promo", "artist" )

    #         db.session.add(example1)
    #         db.session.commit()

    #         setz = db.session.query(Company).filter_by(name="name").first()
    #         self.assertEqual(setz.numCards, 5)
    #         self.assertEqual(setz.promo, "promo")

    #         db.session.delete(example1)
    #         db.session.commit()

    # def test_set_3(self):
    #     with app.test_request_context():
    #         example1 = Set("name", "date", "block", "card",
    #                            5,"promo", "artist" )

    #         db.session.add(example1)
    #         db.session.commit()

    #         setz = db.session.query(Company).filter_by(name="name").first()
    #         self.assertEqual(setz.cards, "card")
    #         self.assertEqual(setz.rDate, "date")

    #         db.session.delete(example1)
    #         db.session.commit()

    # def test_artist_1(self):
    #     with app.test_request_context():
    #         example1 = Artist("name", 10, 5, "card",
    #                            "sets")

    #         db.session.add(example1)
    #         db.session.commit()

    #         artist = db.session.query(Company).filter_by(name="name").first()
    #         self.assertEqual(artist.name, "name")
    #         self.assertEqual(artist.numCards, 10)

    #         db.session.delete(example1)
    #         db.session.commit()

    # def test_artist_2(self):
    #     with app.test_request_context():
    #         example1 = Artist("name", 10, 5, "card",
    #                            "sets")

    #         db.session.add(example1)
    #         db.session.commit()

    #         artist = db.session.query(Company).filter_by(name="name").first()
    #         self.assertEqual(artist.numSets, 5)
    #         self.assertEqual(artist.numCards, 10)

    #         db.session.delete(example1)
    #         db.session.commit()

    # def test_artist_3(self):
    #     with app.test_request_context():
    #         example1 = Artist("name", 10, 5, "card",
    #                            "sets")

    #         db.session.add(example1)
    #         db.session.commit()

    #         artist = db.session.query(Company).filter_by(name="name").first()
    #         self.assertEqual(artist.cards, "card")
    #         self.assertEqual(artist.sets, "sets")

    #         db.session.delete(example1)
    #         db.session.commit()

    # def test_subType_1(self):
    #     with app.test_request_context():
    #         example1 = SubType("name", 10, "link", "cardlink",
    #                            "Thomas", "setlink")

    #         db.session.add(example1)
    #         db.session.commit()

    #         subType = db.session.query(Company).filter_by(name="name").first()
    #         self.assertEqual(subType.name, "name")
    #         self.assertEqual(subType.numCards, 10)

    #         db.session.delete(example1)
    #         db.session.commit()

    # def test_subType_2(self):
    #     with app.test_request_context():
    #         example1 = SubType("name", 10, "link", "cardlink",
    #                            "Thomas", "setlink")

    #         db.session.add(example1)
    #         db.session.commit()

    #         subType = db.session.query(Company).filter_by(name="name").first()
    #         self.assertEqual(subType.cards, "link")
    #         self.assertEqual(subType.exCard, "cardlink")

    #         db.session.delete(example1)
    #         db.session.commit()

    # def test_subType_3(self):
    #     with app.test_request_context():
    #         example1 = SubType("name", 10, "link", "cardlink",
    #                            "Thomas", "setlink")

    #         db.session.add(example1)
    #         db.session.commit()

    #         subType = db.session.query(Company).filter_by(name="name").first()
    #         self.assertEqual(subType.artists, "Thomas")
    #         self.assertEqual(subType.sets, "setlink")

    #         db.session.delete(example1)
    #         db.session.commit()
# ----
# main
# ----

if __name__ == "__main__":  # pragma: no cover
    main()
