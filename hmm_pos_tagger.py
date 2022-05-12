import nltk
from nltk.util import ngrams


class PosTagger:
    def __init__(self, N=3):
        self.start_tag = 'START'
        self.end_tag = 'END'
        self.N = 3  # we hard code this for the moment
        pass

    def fit(self, X):
        self.X = X
        self._generate_prob_counts()

        # TODO: run over X and y and do transition and emission prob counts

    def _generate_prob_counts(self):
        N = self.N

        tag_words = []
        for sentence in self.X:
            tag_words.append((self.start_tag,) * (N - 1))
            for word, tag in sentence:
                tag_words.extend([(tag[:N - 1], word)])
            tag_words.append((self.end_tag,) * (N - 1))

        self.cfd_tag_words = nltk.ConditionalFreqDist(tag_words)
        self.cpd_tag_words = nltk.ConditionalProbDist(self.cfd_tag_words, nltk.MLEProbDist)

        self.tag_words = tag_words
        self.tags = [tag for tag, word in self.tag_words]
        self.distinct_tags = set(self.tags)
        self.cfd_tags = nltk.ConditionalFreqDist(nltk.ngrams(self.tags, N - 1))
        self.cpd_tags = nltk.ConditionalProbDist(self.cfd_tags, nltk.MLEProbDist)

    def _viterbi(self, sample, delimiter=' '):
        sample = sample.split(delimiter)

        viterbi_tag = {}
        viterbi_backpointer = {}

        for tag in self.distinct_tags:
            if tag is self.start_tag:
                continue
            viterbi_tag[tag] = self.cpd_tags[self.start_tag].prob(tag) * self.cpd_tag_words[tag].prob(sample[0])
            viterbi_backpointer[tag] = self.start_tag

        viterbi_main = [viterbi_tag]
        backpointer_main = [viterbi_backpointer]

        curr_best = max(viterbi_tag.keys(), key=lambda tag: viterbi_tag[tag])

        for index in range(1, len(sample)):
            curr_viterbi = {}
            curr_backpointer = {}
            prev_viterbi = viterbi_main[-1]

            for tag in self.distinct_tags:
                if tag is not self.start_tag:
                    prev_best = max(prev_viterbi.keys(),
                                    key=lambda prevtag: prev_viterbi[prevtag] * self.cpd_tags[prevtag].prob(tag) *
                                                        self.cpd_tag_words[tag].prob(sample[index]))
                    curr_viterbi[tag] = prev_viterbi[prev_best] * self.cpd_tags[prev_best].prob(tag) * \
                                        self.cpd_tag_words[tag].prob(sample[index])
                    curr_backpointer[tag] = prev_best

            curr_best = max(curr_viterbi.keys(), key=lambda tag: curr_viterbi[tag])

            viterbi_main.append(curr_viterbi)
            backpointer_main.append(curr_backpointer)

        prev_viterbi = viterbi_main[-1]
        prev_best = max(prev_viterbi.keys(),
                        key=lambda prev_tag: prev_viterbi[prev_tag] * self.cpd_tags[prev_tag].prob(self.end_tag))
        prob_tag_seq = prev_viterbi[prev_best] * self.cpd_tags[prev_best].prob(self.end_tag)

        best_tag_seq = [self.end_tag, prev_best]
        backpointer_main.reverse()

        curr_best = prev_best
        for backpointer in backpointer_main:
            best_tag_seq.append(backpointer[curr_best])
            curr_best = backpointer[curr_best]

        best_tag_seq.reverse()
        return best_tag_seq[1:-1]

    def predict(self, sample):
        return self._viterbi(sample)

    def get_states(self):
        # just tags
        list_tags = ["CC", "CD", "DT", "EX", "FW", "IN", "JJ", "JJR", "LS", "MD", "NN", "NNS", "NNP", "NNPS", "PDT",
                     "POS", "PRP", "PRP$", "RB", "RBR", "RBS", "RP", "SYM", "TO", "UH", "VB", "VBD", "VBG", "VBN",
                     "VBP", "VBZ", "WDT", "WP", "WP$", "WRB"]
        # tags point to descriptions
        dict_tags = {"CC": "Coordinating conjunction",
                     "CD": "Cardinal number",
                     "DT": "Determiner",
                     "EX": "Existential there",
                     "FW": "Foreign word",
                     "IN": "Preposition or subordinating conjunction",
                     "JJ": "Adjective",
                     "JJR": "Adjective, comparative",
                     "JJS": "Adjective, superlative",
                     "LS": "List item marker",
                     "MD": "Modal",
                     "NN": "Noun, singular or mass",
                     "NNS": "Noun, plural",
                     "NNP": "Proper noun, singular",
                     "NNPS": "Proper noun, plural",
                     "PDT": "Predeterminer",
                     "POS": "Possessive ending",
                     "PRP": "Personal pronoun",
                     "PRP$": "Possessive pronoun",
                     "RB": "Adverb",
                     "RBR": "Adverb, comparative",
                     "RBS": "Adverb, superlative",
                     "RP": "Particle",
                     "SYM": "Symbol",
                     "TO": "to",
                     "UH": "Interjection",
                     "VB": "Verb, base form",
                     "VBD": "Verb, past tense",
                     "VBG": "Verb, gerund or present participle",
                     "VBN": "Verb, past participle",
                     "VBP": "Verb, non-3rd person singular present",
                     "VBZ": "Verb, 3rd person singular present",
                     "WDT": "Wh-determiner",
                     "WP": "Wh-pronoun",
                     "WP$": "Possessive wh-pronoun",
                     "WRB": "Wh-adverb"}
        return list_tags
