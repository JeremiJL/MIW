from typing import Literal

from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np

centroids = [(4,4), (4,8), (7,8), (7,4)]

x_centroids = [t[0] for t in centroids]
y_centroids = [t[1] for t in centroids]

print(x_centroids)
print(y_centroids)

plt.scatter(x_centroids, y_centroids)



std = 0.9

X = []
y = []

points_per_class = 50

for i, c in enumerate(centroids):
    data = np.random.randn(points_per_class, 2) * std + c
    X.append(data)
    y.append([i] * points_per_class)

X = np.concatenate(X)
y = np.concatenate(y)

print(X)
print(y)

plt.scatter(X[:,0], X[:,1], c=y)
# plt.show()

class Perceptron:

    def __init__(self, size: int):
        self.size = size
        self.weights = np.random.rand(size) * 2 - 1
        self.bias  = np.random.rand()
        self.lr = 0.1
        self.epochs = 10
        self.activation = lambda x: 1 if x > 0 else 0

    def _forward(self, s: np.ndarray) -> Literal[0,1]:
        dot = np.dot(s, self.weights)
        dot = dot + self.bias
        result = self.activation(dot)
        return result

    def _backwards(self, s: np.ndarray, error: Literal[-1, 0, 1]):
        self.bias += error * self.lr
        for i in range(len(self.weights)):
            self.weights[i] += s[i] * error * self.lr

    def fit(self, X: np.ndarray, y: np.ndarray):
        for sx, sy in zip(X,y):
            y_pred = self._forward(sx)
            error =  sy - y_pred
            self._backwards(sx, error)


    def predict(self,X: np.ndarray) -> np.ndarray:
        retval = [self._forward(s) for s in X]
        return np.array(retval)


p = Perceptron(X.shape[1])

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2)

p.fit(X_train, y_train)
y_pred = p.predict(X_test)

correct = 0

for yt, yp in zip(y_test, y_pred):
    if yt == yp:
        correct += 1

print(correct / len(X_test))
