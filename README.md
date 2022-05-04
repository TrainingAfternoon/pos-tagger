# Part of Speech Tagging using Hidden Markov Model
Developers: Carter Shavitz, John Paul Bunn, Sam Keyser


Hidden Markov Models analyze some system by associating observations with some hidden "state". Using this model, we can begin to predict the next state given our current state and the last *k*-states.

# TODOS:
What we need to deliver this lab
* Data cleaning procedure
  * Unify case
  * Do we keep apostrophes, etc
* Finish transition / emission probability counting for N-grams in NOTEBOOK
* Implement POS tagging in NOTEBOOK
* Implement finished model in `hmm_pos_tagger`
* Presentation
  * Script + power point
    * Introduce algorithm
      * History
      * Other applications of HMM
      * Applications of POS taggers
    * Explain algorithm
      * Mechanics
      * Strength / Weaknesses
        * For general applications
        * For POS tagging
      * Toy examples
    * Show off model with examples
    * Potential applications in the future
    * Ethical concerns
  * Actually record (12-15m)
* Training system for N (other hyperparameters)?
* Use POS-tagging to grade text generator [Sam]

## Presentation
TODO: link


## Resources
### Data
We plan to use the treebank, brown, and conll2000 datasets made available by `nltk.corpus`.


See [this](https://www.kaggle.com/code/gauravduttakiit/pos-tagging-part-3/notebook) for further information.


### Sources
* TODO: insert codecamp article
* TODO: insert link for wikipedia viterbi algo
