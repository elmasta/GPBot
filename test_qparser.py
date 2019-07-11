from qparser import *
import json
import requests

class TestRequestParser:

    REQUESTPARSER = RequestParser()
    REQUESTPARSERTWO = RequestParser()
    REQUESTPARSERTHREE = RequestParser()

    def test_string_to_list(self):

        self.REQUESTPARSER.string_to_list("la,tour eiffel avec")
        self.REQUESTPARSERTWO.string_to_list("l'Arc de Triomphe de l'Étoile")
        self.REQUESTPARSERTHREE.string_to_list("Rue Jeanne-d'Arc (Rouen)")
        assert self.REQUESTPARSER.qprocess ==\
            ["la", "tour", "eiffel", "avec"]
        assert self.REQUESTPARSERTWO.qprocess ==\
            ["l", "'", "arc", "de", "triomphe", "de", "l", "'", "étoile"]
        assert self.REQUESTPARSERTHREE.qprocess ==\
            ["rue", "jeanne-d", "'", "arc", "(", "rouen)"]

    def test_request_reading(self):

        with open("fr.json") as json_file:
            stop_word = json.load(json_file)
        self.REQUESTPARSER.request_reading(stop_word)
        self.REQUESTPARSERTWO.request_reading(stop_word)
        self.REQUESTPARSERTHREE.request_reading(stop_word)
        assert self.REQUESTPARSER.matchlist == [0, 1, 1, 0]
        assert self.REQUESTPARSERTWO.matchlist == [0, 0, 1, 0, 0, 0, 0, 0, 1]
        assert self.REQUESTPARSERTHREE.matchlist == [1, 1, 0, 1, 0, 1]

    def test_stop_word_remover(self):

        with open("fr.json") as json_file:
            stop_word = json.load(json_file)
        self.REQUESTPARSER.stop_word_remover(stop_word)
        self.REQUESTPARSERTWO.stop_word_remover(stop_word)
        self.REQUESTPARSERTHREE.stop_word_remover(stop_word)
        assert self.REQUESTPARSER.qreturn == "Tour_Eiffel"
        assert self.REQUESTPARSERTWO.qreturn == "Arc_de_triomphe_de_l'Étoile"
        assert self.REQUESTPARSERTHREE.qreturn == "Rue_Jeanne-d'Arc_(Rouen)"

    def test_map_url_get(self, monkeypatch):

        results = {"status" : "OK"}

        class MockRequestsGet:
            def __init__(self, url):
                pass
            def json(self):
                return {"status" : "OK"}

        monkeypatch.setattr("requests.get", MockRequestsGet)
        self.REQUESTPARSER.map_url_get(json)
        print(self.REQUESTPARSER.map_found)
        assert self.REQUESTPARSER.map_found == results

    def test_wiki_researcher(self):

        self.REQUESTPARSER.wiki_url_get(json)
        self.REQUESTPARSERTWO.wiki_url_get(json)
        self.REQUESTPARSERTHREE.wiki_url_get(json)
        self.REQUESTPARSER.wiki_researcher()
        self.REQUESTPARSERTWO.wiki_researcher()
        self.REQUESTPARSERTHREE.wiki_researcher()
        assert self.REQUESTPARSER.summary ==\
            "La tour Eiffel  est une tour de fer puddlé de 324 mètres de " +\
            "hauteur (avec antennes) située à Paris, à l’extrémité " +\
            "nord-ouest du parc du Champ-de-Mars en bordure de la Seine " +\
            "dans le 7e arrondissement. Son adresse officielle est 5, " +\
            "avenue Anatole-France. Construite par Gustave Eiffel et ses " +\
            "collaborateurs pour l’Exposition universelle de Paris de " +\
            "1889, et initialement nommée « tour de 300 mètres », ce " +\
            "monument est devenu le symbole de la capitale française, et " +\
            "un site touristique de premier plan : il s’agit du troisième" +\
            " site culturel français payant le plus visité en 2015, avec " +\
            "6,9 millions de visiteurs, en 2011 la cathédrale Notre-Dame " +\
            "de Paris était en tête des monuments à l'accès libre avec " +\
            "13,6 millions de visiteurs estimés mais il reste le monument" +\
            " payant le plus visité au monde,. Depuis son ouverture au " +\
            "public, elle a accueilli plus de 300 millions de visiteurs." +\
            "\nD’une hauteur de 312 mètres à l’origine, la tour Eiffel " +\
            "est restée le monument le plus élevé du monde pendant " +\
            "quarante ans. Le second niveau du troisième étage, appelé " +\
            "parfois quatrième étage, situé à 279,11 mètres, est la " +\
            "plus haute plateforme d'observation accessible au public de " +\
            "l'Union européenne et la deuxième plus haute d'Europe, " +\
            "derrière la tour Ostankino à Moscou culminant à 337 mètres. " +\
            "La hauteur de la tour a été plusieurs fois augmentée par " +\
            "l’installation de nombreuses antennes. Utilisée dans le " +\
            "passé pour de nombreuses expériences scientifiques, elle " +\
            "sert aujourd’hui d’émetteur de programmes radiophoniques et " +\
            "télévisés."
        assert self.REQUESTPARSERTWO.summary ==\
            "L’arc de triomphe de l’Étoile, souvent appelé simplement " +\
            "l’Arc de triomphe, dont la construction, décidée par " +\
            "l'empereur Napoléon Ier, débuta en 1806 et s'acheva en 1836 " +\
            "sous Louis-Philippe, est situé à Paris, dans les 8e, 16e, " +\
            "et 17e arrondissements."
        assert self.REQUESTPARSERTHREE.summary ==\
            "La rue Jeanne-d'Arc est l'artère principale de la rive " +\
            "droite de Rouen."

    def test_geocoding_researcher(self):

        self.REQUESTPARSER.map_url_get(json)
        self.REQUESTPARSERTWO.map_url_get(json)
        self.REQUESTPARSERTHREE.map_url_get(json)
        self.REQUESTPARSER.geocoding_researcher()
        self.REQUESTPARSERTWO.geocoding_researcher()
        self.REQUESTPARSERTHREE.geocoding_researcher()
        assert self.REQUESTPARSER.formatted_adress ==\
            "Champ de Mars, 5 Avenue Anatole France, 75007 Paris, France"
        assert self.REQUESTPARSER.coordinates ==\
            {"lat": 48.85837009999999, "lng": 2.2944813}
        assert self.REQUESTPARSERTWO.formatted_adress ==\
            "Place Charles de Gaulle, 75008 Paris, France"
        assert self.REQUESTPARSERTWO.coordinates ==\
            {"lat": 48.8737917, "lng": 2.2950275}
        assert self.REQUESTPARSERTHREE.formatted_adress ==\
            "Rue Jeanne d'Arc, 76000 Rouen, France"
        assert self.REQUESTPARSERTHREE.coordinates ==\
            {"lat": 49.44356519999999, "lng": 1.0914709}

    def test_quote_picker(self):

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
