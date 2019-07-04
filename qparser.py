class RequestParser:

    def __init__(self):
        self.qreturn = ""
        self.qprocess = ""
        self.matchlist = []

    def string_to_list(self, question):

        self.qprocess = question.lower()
        self.qprocess = self.qprocess.replace("'", " ' ")
        self.qprocess = self.qprocess.replace(",", " ")
        self.qprocess = self.qprocess.replace(".", " ")
        self.qprocess = self.qprocess.split()

    def request_reading(self, stop_word):

        for q_words in self.qprocess:
            for s_words in stop_word:
                if s_words == q_words:
                    self.matchlist.append(0)
                    break
                elif (stop_word.index(s_words) + 1) == len(stop_word):
                    self.matchlist.append(1)

    def stop_word_remover(self, stop_word):

        del self.qprocess[:self.matchlist.index(1)]
        self.qprocess = self.qprocess[::-1]
        self.matchlist = self.matchlist[::-1]
        del self.qprocess[:self.matchlist.index(1)]
        self.qprocess = self.qprocess[::-1]
        for q_word in self.qprocess:
            if q_word == "'":
                self.qreturn += "'"
            for s_words in stop_word:
                if s_words == q_word:
                    self.qreturn += ("+" + s_words)
                    break
                elif (stop_word.index(s_words) + 1) == len(stop_word):
                    self.qreturn += ("+" + q_word.capitalize())
        self.qreturn = self.qreturn.replace("+", "", 1)
        print(self.qreturn)
