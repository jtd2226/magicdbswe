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

from models import Card, Set, Artist, SubType
# -----------
# TestMagic
# -----------


class TestMagic (TestCase):

    # ----
    # CARD
    # ----

    #MODEL EXAMPLE TEST
    # def test_company_model_2(self):
    # """Test querying the database by attribute using simple keywords"""

    # with app.test_request_context():
    #     example1 = Company("id", "name", "summary", "people",
    #                        "city", "finorgs", "twitter", "website", "logo")

    #     db.session.add(example1)
    #     db.session.commit()

    #     company = db.session.query(Company).filter_by(name="name").first()
    #     self.assertEqual(company.city, "city")
    #     self.assertEqual(company.twitter, "twitter")

    #     db.session.delete(example1)
    #     db.session.commit()

    #MODEL METHOD EXAMPLE TEST
    # def test_financial_org_dictionary_1(self):
    # """Test dictionary method of financial org class"""

    # example1 = FinancialOrg("id", "name", "summary", "city", "companies", "twitter",
    #                         "website", "logo")
    # dict_rep = example1.dictionary()

    # self.assertEqual(dict_rep['financial_org_id'], "id")
    # self.assertEqual(dict_rep['name'], "name")
    # self.assertEqual(dict_rep['summary'], "summary")
    # self.assertEqual(dict_rep['city'], "city")

    def test_card_1(self):
        with app.test_request_context():
            example1 = Card("name", "Creature", "Angel", "shine",
                               "Ham", 5, "Red", "pt", "url", "common", "thomas")

            db.session.add(example1)
            db.session.commit()

            card = db.session.query(Company).filter_by(name="name").first()
            self.assertEqual(card.name, "name")
            self.assertEqual(card.mainType, "Creature")

            db.session.delete(example1)
            db.session.commit()

    def test_card_2(self):
        with app.test_request_context():
            example1 = Card("name", "Creature", "Angel", "shine",
                               "Ham", 5, "Red", "pt", "url", "common", "thomas")

            db.session.add(example1)
            db.session.commit()

            card = db.session.query(Company).filter_by(name="name").first()
            self.assertEqual(card.SubType, "Angel")
            self.assertEqual(card.text, "shine")

            db.session.delete(example1)
            db.session.commit()

    def test_card_3(self):
        with app.test_request_context():
            example1 = Card("name", "Creature", "Angel", "shine",
                               "Ham", 5, "Red", "pt", "url", "common", "thomas")

            db.session.add(example1)
            db.session.commit()

            card = db.session.query(Company).filter_by(name="name").first()
            self.assertEqual(card.color, "Red")
            self.assertEqual(card.pt, "pt")

            db.session.delete(example1)
            db.session.commit()

    def test_set_1(self):
        with app.test_request_context():
            example1 = Set("name", "date", "block", "card",
                               5,"promo", "artist" )

            db.session.add(example1)
            db.session.commit()

            setz = db.session.query(Company).filter_by(name="name").first()
            self.assertEqual(setz.name, "name")
            self.assertEqual(setz.block, "block")

            db.session.delete(example1)
            db.session.commit()

    def test_set_2(self):
        with app.test_request_context():
            example1 = Set("name", "date", "block", "card",
                               5,"promo", "artist" )

            db.session.add(example1)
            db.session.commit()

            setz = db.session.query(Company).filter_by(name="name").first()
            self.assertEqual(setz.numCards, 5)
            self.assertEqual(setz.promo, "promo")

            db.session.delete(example1)
            db.session.commit()

    def test_set_3(self):
        with app.test_request_context():
            example1 = Set("name", "date", "block", "card",
                               5,"promo", "artist" )

            db.session.add(example1)
            db.session.commit()

            setz = db.session.query(Company).filter_by(name="name").first()
            self.assertEqual(setz.cards, "card")
            self.assertEqual(setz.rDate, "date")

            db.session.delete(example1)
            db.session.commit()

    def test_artist_1(self):
        with app.test_request_context():
            example1 = Artist("name", 10, 5, "card",
                               "sets")

            db.session.add(example1)
            db.session.commit()

            artist = db.session.query(Company).filter_by(name="name").first()
            self.assertEqual(artist.name, "name")
            self.assertEqual(artist.numCards, 10)

            db.session.delete(example1)
            db.session.commit()
    
    def test_artist_2(self):
        with app.test_request_context():
            example1 = Artist("name", 10, 5, "card",
                               "sets")

            db.session.add(example1)
            db.session.commit()

            artist = db.session.query(Company).filter_by(name="name").first()
            self.assertEqual(artist.numSets, 5)
            self.assertEqual(artist.numCards, 10)

            db.session.delete(example1)
            db.session.commit()

    def test_artist_3(self):
        with app.test_request_context():
            example1 = Artist("name", 10, 5, "card",
                               "sets")

            db.session.add(example1)
            db.session.commit()

            artist = db.session.query(Company).filter_by(name="name").first()
            self.assertEqual(artist.cards, "card")
            self.assertEqual(artist.sets, "sets")

            db.session.delete(example1)
            db.session.commit()

    def test_subType_1(self):
        with app.test_request_context():
            example1 = SubType("name", 10, "link", "cardlink",
                               "Thomas", "setlink")

            db.session.add(example1)
            db.session.commit()

            subType = db.session.query(Company).filter_by(name="name").first()
            self.assertEqual(subType.name, "name")
            self.assertEqual(subType.numCards, 10)

            db.session.delete(example1)
            db.session.commit()

    def test_subType_2(self):
        with app.test_request_context():
            example1 = SubType("name", 10, "link", "cardlink",
                               "Thomas", "setlink")

            db.session.add(example1)
            db.session.commit()

            subType = db.session.query(Company).filter_by(name="name").first()
            self.assertEqual(subType.cards, "link")
            self.assertEqual(subType.exCard, "cardlink")

            db.session.delete(example1)
            db.session.commit()

    def test_subType_3(self):
        with app.test_request_context():
            example1 = SubType("name", 10, "link", "cardlink",
                               "Thomas", "setlink")

            db.session.add(example1)
            db.session.commit()

            subType = db.session.query(Company).filter_by(name="name").first()
            self.assertEqual(subType.artists, "Thomas")
            self.assertEqual(subType.sets, "setlink")

            db.session.delete(example1)
            db.session.commit()
# ----
# main
# ----

if __name__ == "__main__":  # pragma: no cover
    main()
