import numpy as np
from sklearn import datasets


class Logger:
    def info(self, msg):
        print(msg)


class Model:

    def __init__(self, logger, N):
        self.logger = logger
        self.N = N+1
        self.W = np.random.randn(self.N, 1)

    def fit(self, X_train, y_train, epochs=1000, lr=0.001, reg=0.0001):
        X_train = self._add_bias(X_train)
        for epoch in range(epochs+1):
            y_pred = self._forward(X_train)
            dW = (
                np.matmul(X_train.T, (y_pred - y_train))/X_train.shape[0] +
                reg * self.W
            )
            self.W -= lr * dW
            loss = self.loss(y_pred, y_train, reg)
            if epoch%100==0:
                print(f"Epoch: {epoch} loss: {loss}")

    def loss(self, y_pred, y_true, reg):
        ce_loss = -np.sum(y_true * np.log(y_pred) + (1-y_true) * np.log(1-y_pred)) / y_true.shape[0]
        reg_loss = reg*np.sum(self.W**2)
        return ce_loss + reg_loss

    def predict(self, x):
        x = self._add_bias(x)
        return self._forward(x)

    def _add_bias(self, x):
        return np.concatenate( (np.ones(x.shape[0]).reshape(-1, 1), x), 1)

    def _forward(self, x):
        return self._sigmoid(np.matmul(x, self.W))

    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    def get_params(self):
        return self.W

def normalize(X_train: np.array, X_test: np.array):
    means = X_train.mean(axis=0)
    vars = X_train.std(axis=0)
    # log.info(f"means are : {means}, std dev: {vars}")
    # Check if vars are 0 anywhere case.
    X_train = (X_train-means)/vars
    X_test = (X_test-means)/vars
    return X_train, X_test

def train_test_split(x: np.array, y: np.array, split=0.7):
    index = int(len(x)*split)
    return x[:index], x[index:], y[:index].reshape(-1, 1), y[index:].reshape(-1, 1)

if __name__ == "__main__":
    log = Logger()
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

    # log.info(f"features:\n {X}, y:\n: {y}")
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    # log.info(f"X_train:\n {X_train}, X_test:\n: {X_test}, y_train:\n {y_train}, y_test:\n: {y_test}")
    X_train, X_test = normalize(X_train, X_test)
    # log.info(f"X_train:\n {X_train}, X_test:\n: {X_test}")

    model = Model(log, X_train.shape[1])
    model.fit(X_train, y_train)

    print(f"Params: {model.get_params()}")



    
    