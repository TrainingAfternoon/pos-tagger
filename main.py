import nltk
from nltk.util import ngrams
from nltk.corpus import brown, treebank, conll2000
from hmm_pos_tagger import PosTagger

def main():
    nltk.download('brown')

    tagger = PosTagger()

    tagger.fit(brown.tagged_sents())

    sample = 'Doctor Powers is a very neat chap'
    print(tagger.predict(sample))

if __name__ == "__main__":
    main()