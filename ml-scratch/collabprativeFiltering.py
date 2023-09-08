"""
Reference: https://github.com/shik3519/collaborative-filtering/blob/master/cf-scratch-movielens/collaborative%20filtering%20from%20scratch.ipynb
Idea, batch collaborative filtering: andrew ng video
"""

USER = "user_id"
POST = "post_id"
RATING = "rating"

def get_dataset():
    return pd.DataFrame([
        ["user_11", "movie_1", 4],
        ["user_11", "movie_23", 5],
        ["user_2", "movie_23", 5],
        ["user_2", "movie_4", 3],
        ["user_31", "movie_1", 4],
        ["user_31", "movie_23", 4],
        ["user_4", "movie_1", 5],
        ["user_4", "movie_3", 2],
        ["user_52", "movie_1", 1],
        ["user_52", "movie_3", 4],
        ["user_61", "movie_3", 5],
        ["user_7", "movie_23", 1],
        ["user_7", "movie_3", 3],
    ], columns=[USER, POST, RATING])

############################################################

import pandas as pd
import numpy as np

############################################################

class Model:

    def __init__(self, sparse_data, embedding_dim=2):
        self.user_id_mapping = self._get_mapping(sparse_data[USER])
        self.post_id_mapping = self._get_mapping(sparse_data[POST])
        self.reverse_post_mapping = self._get_reverse_mapping(self.post_id_mapping)
        self.reverse_user_mapping = self._get_reverse_mapping(self.user_id_mapping)
    
        self.Y = self._convert_dense_data(sparse_data)
        self.R = np.where(self.Y > 0, 1, 0)
        self.U = self._initialize_embedding(len(self.user_id_mapping), embedding_dim)
        self.V = self._initialize_embedding(len(self.post_id_mapping), embedding_dim)
        self.u_b = self._initialize_bias(len(self.user_id_mapping))
        self.p_b = self._initialize_bias(len(self.post_id_mapping))

        print(f"""
        Shapes:
            self.Y: {self.Y.shape},
            self.R: {self.R.shape},
            self.U: {self.U.shape},
            self.V: {self.V.shape},
            self.u_b: {self.u_b.shape},
            self.p_b: {self.p_b.shape},     
        """)
    
    def fit(self, lr=0.001, alpha=0.0001, epochs=10000):
        for epoch in range(epochs+1):
            predictions = self._forward()
            loss = self.loss(predictions, alpha)
            self._backprop(predictions, lr, alpha)
            if epoch%100==0:
                print(f"epoch: {epoch}, loss: {loss}")

    def loss(self, predictions, alpha):
        loss = 0.5 * np.sum( ( (self.Y - predictions) * self.R)**2 )
        reg_loss = 0.5 * alpha * (
            np.sum(self.U**2) + 
            np.sum(self.V**2) +
            np.sum(self.u_b**2) +
            np.sum(self.p_b**2)
        )
        return loss + reg_loss
    
    def _backprop(self, predictions, lr, alpha):
        dPred = -(self.Y - predictions)*self.R  # u * v
        dU = np.matmul(dPred, self.V) + alpha*self.U
        dV = np.matmul(dPred.T, self.U) + alpha*self.V
        du_b = dPred.sum(axis=1).reshape(-1, 1) + alpha*self.u_b
        dp_b = dPred.sum(axis=0).reshape(-1, 1) + alpha*self.p_b

        self.U -= lr * dU
        self.V -= lr * dV
        self.u_b -= lr * du_b
        self.p_b -= lr * dp_b

    def _forward(self):
        return np.matmul(self.U, self.V.T) + self.u_b + self.p_b.T

    def predict(self, userid):
        if userid not in self.user_id_mapping:
            raise Exception("User not found")
        
        user_emb = self.U[self.user_id_mapping[userid]].reshape(-1, 1)
        predicted = np.matmul(self.V, user_emb) + self.p_b
        predicted = predicted.squeeze()
        best_post_idx = predicted.argmax(axis=0)
        print(f"best movies: {self.reverse_post_mapping[best_post_idx]}")
        
    def _convert_dense_data(self, sparse_data):
        num_users = len(self.user_id_mapping)
        num_posts = len(self.post_id_mapping)

        dense_data = np.zeros( (num_users, num_posts) )
        for _, row in sparse_data.iterrows():
            user_idx = self.user_id_mapping[row[USER]]
            post_idx = self.post_id_mapping[row[POST]]
            dense_data[user_idx][post_idx] = row[RATING]
        return dense_data

    def _get_mapping(self, id_list: list):
        all_ids = list(set(id_list))
        return {id:i for i, id in enumerate(all_ids)}

    def _initialize_embedding(self, sz, emb_dim):
        return np.random.randn(sz, emb_dim)
    
    def _initialize_bias(self, sz):
        return np.random.randn(sz, 1)

    def _get_reverse_mapping(self, d):
        return {v:k for k, v in d.items()}


if __name__ == "__main__":
    data = get_dataset()
    model = Model(data)
    model.predict("user_11")
    model.fit()
    model.predict("user_11")
    model.predict("user_11")
    model.predict("user_11")
    model.predict("user_11")
    model.predict("user_11")
    model.predict("user_11")
    model.predict("user_11")










