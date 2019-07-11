import requests
from random import randrange

class RequestParser:
    """Is charged to parse user's request and retrieve infos from API"""

    QUOTE_LIST = [
        "Hé mais je connais cet endroit, c'est la où. . . zzz . . . Hein " +\
        "quoi? tu veux plus d'informations? Tiens prends cet encyclop. . . " +\
        "zzz",
        "C'est ici que j'ai rencontré ma femme, je crois. . . J'avais une" +\
            " femme? Ah sinon j'ai trouvé ça dans mon encyclopédie:",
        "Savais-tu que l'inventeur du kiwi habitait ici? Ah sacré Billy! As" +\
            "-tu connus les encyclopédies papier? Voilà à quoi ça " +\
            "ressemble à l'intérieur:",
        "I AM ERROR bzzzt bzzzzt encyclopédie:",
        "zzz . . . J'avais froid, je n'avais plus de munitions et les" +\
            " Allemands allaient me tomber dessus. . . zzz . . .Hein quoi?" +\
            " Ah oui, c'est un joli coin! Tu as de la chance sinon, j'ai" +\
            " mon encyclopédie avec moi:",
        "Encore un lieu que ces ordures communiste n'auront pas! Ils" +\
            " n'auront pas non plus cette encyclopédie que j'ai dans les" +\
            " mains!",
        "Moi vivant tu n'iras jamais dans ce lieu de perdition! Ah j'ai" +\
            " ça aussi dans mon encyclopédie! Je t'avais raconté comment" +\
            " je l'avais gagné dans un jeu télévisé?"
    ]

    def __init__(self):
        self.qreturn = ""
        self.qprocess = ""
        self.matchlist = []
        self.formatted_adress = ""
        self.summary = ""
        self.coordinates = {"lat": 0, "lng": 0}
        self.error = 1
        self.wiki_found = {}
        self.map_found = {}
        self.quote = ""

    def string_to_list(self, question):
        """remove some special characters and change string to list"""

        self.qprocess = question.lower()
        self.qprocess = self.qprocess.replace("'", " ' ")
        self.qprocess = self.qprocess.replace("(", " ( ")
        self.qprocess = self.qprocess.replace(",", " ")
        self.qprocess = self.qprocess.replace(".", " ")
        self.qprocess = self.qprocess.replace("!", " ")
        self.qprocess = self.qprocess.replace("?", " ")
        self.qprocess = self.qprocess.split()

    def request_reading(self, stop_word):
        """read the word list to check which word is a stop word and which word
        is a keyword"""

        for q_words in self.qprocess:
            for s_words in stop_word:
                if s_words == q_words:
                    self.matchlist.append(0)
                    break
                elif (stop_word.index(s_words) + 1) == len(stop_word):
                    self.matchlist.append(1)

    def stop_word_remover(self, stop_word):
        """Remove stop words that are not between key words"""

        del self.qprocess[:self.matchlist.index(1)]
        self.qprocess = self.qprocess[::-1]
        self.matchlist = self.matchlist[::-1]
        del self.qprocess[:self.matchlist.index(1)]
        self.qprocess = self.qprocess[::-1]
        for q_word in self.qprocess:
            for s_words in stop_word:
                if s_words == q_word:
                    self.qreturn += ("_" + s_words)
                    break
                elif (stop_word.index(s_words) + 1) == len(stop_word):
                    self.qreturn += ("_" + q_word.capitalize())
        self.qreturn = self.qreturn.replace("_", "", 1)
        self.qreturn = self.qreturn.replace("_'_", "'")
        self.qreturn = self.qreturn.replace("(_", "(")

    def map_url_get(self, json):
        """retrieve a json file from google api"""

        map_url = "https://maps.googleapis.com/maps/api/geocode/json?" +\
        "address=" + self.qreturn + "&region=fr&key=" +\
        "AIzaSyAdgDy_GLOqvdeqcoXJE5rVTiaGzq02HXU"
        response = requests.get(map_url)
        self.map_found = json.loads(response.text)

    def wiki_url_get(self, json):
        """retrieve a json file from wikipedia api"""

        wiki_url = "https://fr.wikipedia.org/w/api.php?format=json&action" +\
        "=query&prop=coordinates|extracts&exintro&explaintext&titles=" +\
        self.qreturn
        response = requests.get(wiki_url)
        self.wiki_found = json.loads(response.text)

    def geocoding_researcher(self):
        """retrieve coordinates and adress from a json file"""

        found_list = self.map_found["results"]
        try:
            found_list = found_list[0]
            for key, value in found_list.items():
                if key == "formatted_address":
                    self.formatted_adress = value
                if key == "geometry":
                    self.coordinates = value["location"]
                    self.error = 0
                    break
        except IndexError:
            pass

    def wiki_researcher(self):
        """retrieve adress summary from a json file"""

        end_recur = 0
        while end_recur == 0:
            for key, value in self.wiki_found.items():
                if key == "extract":
                    if not value:
                        self.summary = ". . . Hum il n'y a rien dans " +\
                                       "mon encyclopédie, étrange. . ."
                    else:
                        self.summary = value
                    end_recur = 1
                elif key == "missing":
                    self.summary = ". . . Hum il n'y a rien dans mon " +\
                                   "encyclopédie, étrange. . ."
                    end_recur = 1
                elif isinstance(value, dict):
                    self.wiki_found = value

    def quote_picker(self):
        """pick a random quote from the quote list"""

        quote_list = self.QUOTE_LIST.copy()
        self.quote = quote_list.pop(randrange(len(quote_list)))
