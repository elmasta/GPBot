import json

def f_parser(question):

    with open("fr.json") as json_file:
        stop_word = json.load(json_file)

    if question.replace(" ", "").isalpha() is True:
        qprocess = question.lower()
        qprocess = qprocess.split()
        qreturn = []

        for q_word in qprocess:
            for s_words in stop_word:
                if s_words == q_word:
                    break
                elif (stop_word.index(s_words) + 1) == len(stop_word):
                    qreturn.append(qprocess[qprocess.index(q_word)].capitalize())
        qreturn = "+".join(qreturn)

    else:
        qreturn = "error"

    return qreturn
