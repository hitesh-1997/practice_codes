import numpy as np
import pandas as pd


class Kmeans:

    def __init__(self, k):
        self.k = k

    def _init_centroids(self, X_train):
        self.centroids = X_train[:self.k]

    def fit(self, X_train, epochs=1000):
        self._init_centroids(X_train)
        
        for epoch in range(epochs+1):
            distances = []
            for i in range(self.k):
                vectors = X_train - self.centroids[i]
                distances.append(np.sqrt(np.sum(vectors**2, axis=1)))
                
            all_distance_arr = np.c_[distances].T
            indexs = all_distance_arr.argmax(axis=1)

            new_centroids = []
            for i in range(self.k):
                idxs = (indexs==i)
                if idxs.sum()==0:
                    new_centroids.append(self.centroids[i])
                else:
                    new_centroids.append(X_train[idxs].mean(axis=0))
            self.centroids = np.array(new_centroids)
            if epoch % 100 == 0:
                print(f"epoch: {epoch}, centroid: \n{self.centroids}")


def normalize(X_train: np.array, X_test: np.array):
    means = X_train.mean(axis=0)
    vars = X_train.std(axis=0)
    X_train = (X_train-means)/vars
    X_test = (X_test-means)/vars
    return X_train, X_test

def train_test_split(x: np.array, y: np.array, split=0.9):
    index = int(len(x)*split)
    return x[:index], x[index:], y[:index].reshape(-1, 1), y[index:].reshape(-1, 1)

if __name__ == "__main__":
    M, N = 1000, 5
    # X = np.random.rand(M, N)
    X = np.random.randint( 0, 6, (M, N) )
    y = np.random.randint(0, 2, (M, 1))
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    # X_train, X_test = normalize(X_train, X_test)
    model = Kmeans(k=3)
    model.fit(X_train)


