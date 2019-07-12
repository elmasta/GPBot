from qparser import *
import json
import requests

class TestRequestParser:
    """The class test each method from class RequestParser from
    qparser.py"""

    REQUESTPARSER = RequestParser()
    REQUESTPARSERTWO = RequestParser()
    REQUESTPARSERTHREE = RequestParser()
    REQUESTPARSERFOUR = RequestParser()

    def test_string_to_list(self):
        """check if the methode string_to_list from qparser.py
        works"""

        self.REQUESTPARSER.string_to_list("la,tour eiffel avec")
        self.REQUESTPARSERTWO.string_to_list("l'Arc de Triomphe de l'Étoile")
        self.REQUESTPARSERTHREE.string_to_list("Rue Jeanne-d'Arc (Rouen)")
        self.REQUESTPARSERFOUR.string_to_list("<poste>")
        assert self.REQUESTPARSER.qprocess ==\
            ["la", "tour", "eiffel", "avec"]
        assert self.REQUESTPARSERTWO.qprocess ==\
            ["l", "'", "arc", "de", "triomphe", "de", "l", "'", "étoile"]
        assert self.REQUESTPARSERTHREE.qprocess ==\
            ["rue", "jeanne-d", "'", "arc", "(", "rouen)"]
        assert self.REQUESTPARSERFOUR.qtoshow == "poste"

    def test_request_reading(self):
        """check if the methode stop_request_reading from qparser.py
        works"""

        with open("fr.json") as json_file:
            stop_word = json.load(json_file)
        self.REQUESTPARSER.request_reading(stop_word)
        self.REQUESTPARSERTWO.request_reading(stop_word)
        self.REQUESTPARSERTHREE.request_reading(stop_word)
        assert self.REQUESTPARSER.matchlist == [0, 1, 1, 0]
        assert self.REQUESTPARSERTWO.matchlist == [0, 0, 1, 0, 1, 0, 0, 0, 1]
        assert self.REQUESTPARSERTHREE.matchlist == [1, 1, 0, 1, 0, 1]

    def test_stop_word_remover(self):
        """check if the methode stop_word_remover from qparser.py
        works"""

        with open("fr.json") as json_file:
            stop_word = json.load(json_file)
        self.REQUESTPARSER.stop_word_remover(stop_word)
        self.REQUESTPARSERTWO.stop_word_remover(stop_word)
        self.REQUESTPARSERTHREE.stop_word_remover(stop_word)
        assert self.REQUESTPARSER.qreturn == "Tour_Eiffel"
        assert self.REQUESTPARSERTWO.qreturn == "Arc_de_Triomphe_de_l'Étoile"
        assert self.REQUESTPARSERTHREE.qreturn == "Rue_Jeanne-d'Arc_(Rouen)"

    def test_geocoding_researcher(self, monkeypatch):
        """check if the method wiki_researcher from qparser.py works
        without using Google API"""

        class MockRequestsGet:
            def __init__(self, arg):
                pass
            def mock_json(self):
                return {
                    "results" : [
                        {
                            "address_components" : [
                                {
                                    "long_name" : "Champ de Mars",
                                    "short_name" : "Champ de Mars",
                                    "types" : [ "establishment",
                                                "point_of_interest" ]
                                },
                                {
                                    "long_name" : "5",
                                    "short_name" : "5",
                                    "types" : [ "street_number" ]
                                },
                                {
                                    "long_name" : "Avenue Anatole France",
                                    "short_name" : "Avenue Anatole France",
                                    "types" : [ "route" ]
                                },
                                {
                                    "long_name" : "Paris",
                                    "short_name" : "Paris",
                                    "types" : [ "locality", "political" ]
                                },
                                {
                                    "long_name" : "Arrondissement de Paris",
                                    "short_name" : "Arrondissement de Paris",
                                    "types" : [ "administrative_area_level_2",
                                                "political" ]
                                },
                                {
                                    "long_name" : "Île-de-France",
                                    "short_name" : "Île-de-France",
                                    "types" : [ "administrative_area_level_1",
                                                "political" ]
                                },
                                {
                                    "long_name" : "France",
                                    "short_name" : "FR",
                                    "types" : [ "country", "political" ]
                                },
                                {
                                    "long_name" : "75007",
                                    "short_name" : "75007",
                                    "types" : [ "postal_code" ]
                                }
                            ],
                            "formatted_address" : "Champ de Mars, 5 Avenue " +\
                                "Anatole France, 75007 Paris, France",
                            "geometry" : {
                                "location" : {
                                    "lat" : 48.85837009999999,
                                    "lng" : 2.2944813
                                },
                                "location_type" : "ROOFTOP",
                                "viewport" : {
                                    "northeast" : {
                                        "lat" : 48.8597190802915,
                                        "lng" : 2.295830280291502
                                    },
                                    "southwest" : {
                                        "lat" : 48.8570211197085,
                                        "lng" : 2.293132319708498
                                    }
                                }
                            },
                            "partial_match" : "true",
                            "place_id" : "ChIJLU7jZClu5kcR4PcOOO6p3I0",
                            "plus_code" : {
                                "compound_code" : "V75V+8Q Paris, France",
                                "global_code" : "8FW4V75V+8Q"
                            },
                            "types" : [ "establishment", "point_of_interest",
                                        "premise" ]
                        }
                    ],
                }

        monkeypatch.setattr("json.loads", MockRequestsGet.mock_json)
        self.REQUESTPARSERTWO.geocoding_researcher(json)
        assert self.REQUESTPARSERTWO.coordinates ==\
            {"lat" : 48.85837009999999, "lng" : 2.2944813}
        assert self.REQUESTPARSERTWO.formatted_adress == "Champ de Mars, 5 " +\
            "Avenue Anatole France, 75007 Paris, France"

    def test_wiki_researcher(self, monkeypatch):
        """check if the method wiki_researcher from qparser works
        without using Wikipedia's API"""

        self.REQUESTPARSERTWO.summary =\
            ". . . Hum il n'y a rien dans mon encyclopédie, étrange. . ."

        class MockRequestsGet:
            def __init__(self, arg):
                pass
            def mock_json(self):
                return {
                    "batchcomplete": "",
                    "query": {
                        "normalized": [
                            {
                                "from": "Arc_de_Triomphe_de_l'Étoile",
                                "to": "Arc de Triomphe de l'Étoile"
                            }
                        ],
                        "pages": {
                            "3687153": {
                                "pageid": 3687153,
                                "ns": 0,
                                "title": "Arc de Triomphe de l'Étoile",
                                "extract": ""
                            }
                        }
                    }
                }

        monkeypatch.setattr("json.loads", MockRequestsGet.mock_json)
        self.REQUESTPARSERTWO.wiki_researcher(json)
        assert self.REQUESTPARSERTWO.summary ==\
            ". . . Hum il n'y a rien dans mon encyclopédie, étrange. . ."

    def test_quote_picker(self):
        """check if the method quote_picker from qparser works"""

        self.REQUESTPARSER.quote_picker()
        self.REQUESTPARSERTWO.quote_picker()
        self.REQUESTPARSERTHREE.quote_picker()
        quote_one = ""
        quote_two = ""
        quote_three = ""
        for quotes in self.REQUESTPARSER.QUOTE_LIST:
            if quotes == self.REQUESTPARSER.quote:
                quote_one = quotes
        for quotes in self.REQUESTPARSERTWO.QUOTE_LIST:
            if quotes == self.REQUESTPARSERTWO.quote:
                quote_two = quotes
        for quotes in self.REQUESTPARSERTHREE.QUOTE_LIST:
            if quotes == self.REQUESTPARSERTHREE.quote:
                quote_three = quotes
        assert self.REQUESTPARSER.quote == quote_one
        assert self.REQUESTPARSERTWO.quote == quote_two
        assert self.REQUESTPARSERTHREE.quote == quote_three
