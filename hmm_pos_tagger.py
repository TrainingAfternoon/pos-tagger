import numpy as np
import pandas as pd
from viterbi import viterbi


class PosTagger:
    def __init__(self):
        pass

    def fit(self, X, y):
        self.X = X
        self.y = y

        # TODO: run over X and y and do transition and emission prob counts

    def predict(self, X):
        #obs = X #- array of sentences
        #states = self.get_states()
        #start_p = 
        #trans_p
        #emit_p
        #return viterbi(obs, states, start_p, trans_p, emit_p)
        # TODO: return a vector with the part-of-speech of each token in X
        pass

    def get_states(self):
        #just tags
        list_tags = ["CC", "CD", "DT", "EX", "FW", "IN", "JJ", "JJR", "LS", "MD", "NN", "NNS", "NNP","NNPS","PDT","POS","PRP","PRP$","RB","RBR","RBS","RP","SYM","TO","UH","VB","VBD","VBG","VBN","VBP","VBZ","WDT","WP","WP$","WRB"]
        #tags point to descriptions
        dict_tags = {"CC":"Coordinating conjunction",
                    "CD":"Cardinal number",
                    "DT":"Determiner",
                    "EX":"Existential there",
                    "FW":"Foreign word",
                    "IN":"Preposition or subordinating conjunction",
                    "JJ":"Adjective",
                    "JJR":"Adjective, comparative",
                    "JJS":"Adjective, superlative",
                    "LS":"List item marker",
                    "MD":"Modal",
                    "NN":"Noun, singular or mass",
                    "NNS":"Noun, plural",
                    "NNP":"Proper noun, singular",
                    "NNPS":"Proper noun, plural",
                    "PDT":"Predeterminer",
                    "POS":"Possessive ending",
                    "PRP":"Personal pronoun",
                    "PRP$":"Possessive pronoun",
                    "RB":"Adverb",
                    "RBR":"Adverb, comparative",
                    "RBS":"Adverb, superlative",
                    "RP":"Particle",
                    "SYM":"Symbol",
                    "TO":"to",
                    "UH":"Interjection",
                    "VB":"Verb, base form",
                    "VBD":"Verb, past tense",
                    "VBG":"Verb, gerund or present participle",
                    "VBN":"Verb, past participle",
                    "VBP":"Verb, non-3rd person singular present",
                    "VBZ":"Verb, 3rd person singular present",
                    "WDT":"Wh-determiner",
                    "WP":"Wh-pronoun",
                    "WP$":"Possessive wh-pronoun",
                    "WRB":"Wh-adverb"}
        return list_tags