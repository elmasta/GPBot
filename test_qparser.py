from qparser import *
import json

class TestRequestParser:

    REQUESTPARSER = RequestParser()
    REQUESTPARSERTWO = RequestParser()
    REQUESTPARSERTHREE = RequestParser()

    def test_string_to_list(self):

        self.REQUESTPARSER.string_to_list("la,tour eiffel avec")
        self.REQUESTPARSERTWO.string_to_list("l'Arc de Triomphe de l'Étoile")
        self.REQUESTPARSERTHREE.string_to_list("Rue Jeanne-d'Arc (Rouen)")
        assert self.REQUESTPARSER.qprocess == ["la", "tour", "eiffel", "avec"]
        assert self.REQUESTPARSERTWO.qprocess == ["l", "'", "arc", "de", "triomphe", "de", "l", "'", "étoile"]
        assert self.REQUESTPARSERTHREE.qprocess == ["rue", "jeanne-d", "'", "arc", "(", "rouen)"]

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
