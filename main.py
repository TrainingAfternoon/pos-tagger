import os
import nltk
from nltk.corpus import brown, treebank, conll2000
from nltk.corpus.util import LazyCorpusLoader
from gui import PosTaggerGui
from hmm_pos_tagger import PosTagger


def main():
    has_brown = False
    for path in nltk.data.path:
        has_brown = os.path.exists(os.path.join(path, 'corpora', 'brown'))
        if has_brown:
            break

    if not has_brown:
        nltk.download('brown')

    tagger = PosTagger()
    tagger.fit(brown.tagged_sents())

    gui = PosTaggerGui(tagger)
    gui.start()


if __name__ == "__main__":
    main()
