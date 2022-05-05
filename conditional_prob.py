import math
import itertools
import functools

# convenience method
def increment_dict_val(dict, val):
    dict[val] = dict.get(val, 0) + 1

class ConditionalProbability:
    start_tag = '!@#$START$#@!' # Pick some arbitrary string that is not likely to be naturally embedded into our text data

    k = 10 # k fold hyperparameter

    def __init__(self, X, N=3):
        assert(N >= 2)

        # Init dataset and hyperparameters
        self.X = X
        #self.y = y
        self.N = N

        # P(Wi|Ck)
        self.words_given_pos = {}

        # conditional probability of P(Xi+N|Xi+N-1...Xi)
        self.full_ngram = {}

        # maps word to set of tags associated with it
        self.word_to_tag = {}

        # maps (word, tag) pairings to # of appearances
        self.word_tag_count = {}

        # tracks the number of time a tag has appeared
        self.tag_count = {{}}

        # counts the occurrence of n-gram of tags
        self.ngram_counts = {}

        # counts the occurrences of (n-1)-grams of tags
        self.subset_ngram_counts = {}

        # set of all tags we've seen
        self.tags = set()

        # set of all words
        self.words = set()

        ''' BACK-OFF PROB '''
        self.transition_backoff = {}
        self.emission_backoff = {}

        ''' SINGLETON COUNTS '''
        self.transition_singleton = {}
        self.emission_singleton = {}

        ''' 1-COUNT SMOOTHED PROB '''
        self.transition_one_count = {}
        self.emission_smoothed = {}

        self.n = 0 #TODO: what am I

    def calculate_probabilities(self):
        self.populate_dictionaries()
        self.CFD_word_given_tag()
        self.CFD_ngram_tags()
        self.backoff_probabilities()
        self.singleton_counts()
        self.smooth_probabilities()
        #self._save()

    def populate_dictionaries(self):
        self.pos_tags = set()

        start_tag = ConditionalProbability.start_tag
        for sentence in X:
            for iter in range(0, self.N-1): # We need N-1 start characters to support N-grams
                sentence.insert(0, (start_tag, start_tag))

            start_idx = self.N-1
            for idx in range(start_idx, len(sentence)):
                ngram = tuple([sentence[jdx][1] for jdx in range(idx-N-1, idx+1)])
                sub_ngram = ngram[:-1]

                self.ngram_counts[ngram] = self.ngram_counts.get(ngram, 0) + 1
                self.subset_ngram_counts[sub_ngram] = self.subset_ngram_counts.get(sub_ngram, 0) + 1

            for word, tag in sentence:
                self.n += 1

                # do back off counts
                self.transition_backoff[tag] = self.transition_backoff.get(tag, 0) + 1
                self.emission_backoff[word] = self.emission_backoff.get(word, 0) + 1

                self.tags.add(tag)
                self.words.add(word)

                increment_dict_val(self.word_tag_count, (word, tag))
                increment_dict_val(self.tag_count, tag)

                if word not in self.word_to_tag:
                    self.word_to_tag[word] = set()
                self.word_to_tag[word].add(tag)

    def backoff_probabilities(self):
        V = len(self.tags)

        for word in self.emission_backoff:
            self.emission_backoff[word] = float(1 + self.emission_backoff[word]) / float(self.n + V)

        for tag in self.transition_backoff:
            self.transition_backoff[tag] = float(self.transition_backoff[tag]) / float(self.n)

    def singleton_counts(self):
        for permutation in itertools.permutations(self.tags):
            if permutation in self.ngram_counts and self.ngram_counts[permutation] == 1:
                increment_dict_val(self.transition_singleton, permutation[1:])


        for word in self.words:
            for tag in self.tags:
                word_tag = (word, tag)
                if word_tag in self.word_tag_count and self.word_tag_count[word_tag] == 1:
                    increment_dict_val(self.emission_singleton, tag)

    def smooth_probabilities(self):
        start_idx = self.N - 1

        for sentence in self.X:
            for idx in range(start_idx, len(sentence)):
                ngram = tuple([sentence[jdx][1] for jdx in range(idx-N-1, idx+1)])
                sub_ngram = ngram[:-1]
                lamda = 1 + self.transition_singleton.get(sub_ngram, 0)
                self.transition_one_count[ngram] = math.log(float(self.ngram_counts[ngram] + lamda * self.transition_backoff[sentence[idx][1]]) / float(self.subset_ngram_counts[sub_ngram] + lamda))

        for word, tag_set in self.word_to_tag.items():
            for tag in tag_set:
                lamda = 1 + self.emission_singleton.get(tag, 0)
                self.emission_smoothed[(word, tag)] = math.log(float(self.word_tag_count[(word, tag)] + lamda * self.emission_backoff[word]) / float(self.tag_count[tag] + lamda))

    def CFD_word_given_tag(self):
        '''
        P(word|tag)
        :return:
        '''
        for word, tag_set in self.word_to_tag.items():
            for tag in tag_set:
                self.words_given_pos[(word, tag)] = math.log(float(self.word_tag_count[(word, tag)]) / float(self.tag_count[tag]))

    def CFD_ngram_tags(self):
        '''
        probability of a tag s given last n-1 tags
        :return:
        '''
        start_idx = self.N-1
        V = len(self.tags)

        for sentence in X:
            for idx in range(start_idx, len(sentence)):
                ngram = tuple([sentence[jdx][1] for jdx in range(idx-N-1, idx+1)])
                sub_ngram = ngram[:-1]

                self.full_ngram[ngram] = math.log(float(1 + self.ngram_counts[ngram]) / float(V + self.subset_ngram_counts[sub_ngram]))
