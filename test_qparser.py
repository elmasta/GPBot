from qparser import *
import json

class TestRequestParser:

    REQUESTPARSER = RequestParser()
    REQUESTPARSERTWO = RequestParser()

    def test_string_to_list(self):

        self.REQUESTPARSER.string_to_list("la,tour eiffel avec")
        assert self.REQUESTPARSER.qprocess == ["la", "tour", "eiffel", "avec"]

    def test_request_reading(self):

        with open("fr.json") as json_file:
            stop_word = json.load(json_file)
        self.REQUESTPARSER.request_reading(stop_word)
        assert self.REQUESTPARSER.matchlist == [0, 1, 1, 0]

    def test_stop_word_remover(self):

        with open("fr.json") as json_file:
            stop_word = json.load(json_file)
        self.REQUESTPARSER.stop_word_remover(stop_word)
        assert self.REQUESTPARSER.qreturn == "Tour_Eiffel"

    def test_string_to_list_two(self):

        self.REQUESTPARSERTWO.string_to_list("l'Arc de Triomphe de l'Étoile")
        assert self.REQUESTPARSERTWO.qprocess == ["l", "'", "arc", "de", "triomphe", "de", "l", "'", "étoile"]

    def test_request_reading_two(self):

        with open("fr.json") as json_file:
            stop_word = json.load(json_file)
        self.REQUESTPARSERTWO.request_reading(stop_word)
        assert self.REQUESTPARSERTWO.matchlist == [0, 0, 1, 0, 0, 0, 0, 0, 1]

    def test_stop_word_remover_two(self):

        with open("fr.json") as json_file:
            stop_word = json.load(json_file)
        self.REQUESTPARSERTWO.stop_word_remover(stop_word)
        assert self.REQUESTPARSERTWO.qreturn == "Arc_de_triomphe_de_l'Étoile"
