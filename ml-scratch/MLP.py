import numpy as np
from sklearn import datasets

"""
Ref: https://towardsdatascience.com/lets-code-a-neural-network-in-plain-numpy-ae7e74410795
NN:
layers:
inp - l1 ->  l2 -> l3 -> out
  d   (n1)  (n2)  (n3)
      (a1)  (a2) .....
w:    n1*d  n2*n1  n3*n2 ... so on
layers: [(sz, activation)] 
"""

RELU = 'relu'
SIGMOID = 'sigmoid'

class Model:

    def __init__(self, N, layers):
        self.N = N+1
        self.nn = []
        last_dim = N
        for nodes, activate in layers:
            self.nn.append({
                'nodes': nodes,
                'activation': activate,
                'weight': self.random.randn(nodes, last_dim)

            })
            last_dim = nodes

        self.nn.append({
            'nodes': 1,
            'activation': SIGMOID,
            'weight': self.random.randn(1, last_dim)
        })

    def fit(self, X_train, y_train, epochs=1000, lr=0.001, reg=0.0001):
        X_train = self._add_bias(X_train)
        for epoch in epochs:
            y_pred = self._forward(self, X_train)
            loss = self.loss(y_train, y_pred)
            print(f"Epoch: {epoch}, loss: {loss}")
            # backprop
            # ToDo: Saw solution, so did not continue



    def loss(self, y_true, y_pred):
        return -np.mean(y_true * y_pred + (1 - y_true) * (1 - y_pred))

    def predict_proba(self, x):
        x_with_bias = self._add_bias(x)
        return self.forward(x_with_bias)

    # Helpers
    def _forward(self, x, train=False):
        out = x
        for layer in self.nn:
            weight, activation = layer['weight'], layer['activation']
            out = np.matmul(out, weight.T)
            if activation==RELU:
                out = self._sigmoid(out)
            elif activation==SIGMOID:
                out = self._relu(out)
        return out
        
    def _add_bias(self, x):
        return np.concatenate((np.ones(len(x), 1), x), axis=1)

    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def _relu(self, x):
        return np.max(0, x)
    
    def _sigmoid_backward(self, dA, x):
        sig = self._sigmoid(x)
        return dA * sig * (1-sig)

    def _relu_backprop(self, dA, x):
        return dA * np.where(x>0, 1, 0)


def normalize(X_train: np.array, X_test: np.array):
    means = X_train.mean(axis=0)
    vars = X_train.std(axis=0)
    X_train = (X_train-means)/vars
    X_test = (X_test-means)/vars
    return X_train, X_test

def train_test_split(x: np.array, y: np.array, split=0.7):
    index = int(len(x)*split)
    return x[:index], x[index:], y[:index].reshape(-1, 1), y[index:].reshape(-1, 1)

if __name__ == "__main__":
    USE_RANDOM_DATA = True
    if USE_RANDOM_DATA:
        M, N = 1000, 10
        X = np.random.randint(0, 10, size=(M, N))
        y = np.random.randint(0, 2, size=(len(X), 1))
    else:
        iris = datasets.load_iris()
        X = iris.data[:, :2]
        y = (iris.target != 0) * 1
        M, N = X.shape[0], X.shape[1]

    X_train, X_test, y_train, y_test = train_test_split(X, y)
    X_train, X_test = normalize(X_train, X_test)

    layers = [
        [16, RELU],
        [32, RELU]
    ]
    model = Model(X_train.shape[1], layers)


    
    