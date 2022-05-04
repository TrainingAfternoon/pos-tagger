import numpy as np
import pandas as pd


class PosTagger:
    def __init__(self):
        pass

    def fit(self, X, y):
        self.X = X
        self.y = y

        # TODO: run over X and y and do transition and emission prob counts

    def predict(self, X):
        # TODO: return a vector with the part-of-speech of each token in X
        pass