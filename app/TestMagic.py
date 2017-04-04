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
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from models import db, Card, Set, Artist, Subtype

# -----------
# TestMagic
# -----------


class TestMagic (TestCase):

    # ----
    # CARD
    # ----
    def test_card_1(self):

    # cardId = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(MED_LEN))
    # mainType = db.Column(db.String(NAME_LEN))
    # subtype = db.Column(db.String(MED_LEN), db.ForeignKey('subtypes.name'))
    # text = db.Column(db.String(TEXT_LEN), nullable=True)
    # expansionSet = db.Column(db.String(STG_LEN), db.ForeignKey('Sets.code'))
    # manaCost = db.Column(db.Integer, nullable=True)
    # color = db.Column(db.String(SHORT_LEN), nullable=True)
    # power = db.Column(db.Integer, nullable=True)
    # toughness = db.Column(db.Integer, nullable=True)
    # art = db.Column(db.String(MED_LEN))
    # rarity = db.Column(db.String(STG_LEN))
    # artist = db.Column(db.String(MED_LEN), db.ForeignKey('Artists.name'))
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://magicdb:mtgdb@35.188.87.113:5432/magicdb'
        db = SQLAlchemy(app)

        example1 = Card(123, 'name', 'Creature', 'Angel', 'shine', '1234567891', 5, 'Red', 1, 1, 'url', 'common', 'thomas')
        db.session.add(example1)
        db.session.commit()

        card = db.session.query(Card).filter_by(name="name").first()
        self.assertEqual(card.name, "name")
        self.assertEqual(card.mainType, "Creature")

        db.session.delete(example1)
        db.session.commit()

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
