import numpy as np
from test import Util

def sigmoid(x):
    return 1.0/(1.0 + np.exp(-x))

def sigmoid_prime(x):
    return sigmoid(x)*(1.0-sigmoid(x))

def tanh(x):
    return np.tanh(x)

def tanh_prime(x):
    return 1.0 - x**2


class NeuralNetwork:

    def __init__(self, layers, activation='sigmoid'):
        if activation == 'sigmoid':
            self.activation = sigmoid
            self.activation_prime = sigmoid_prime
        elif activation == 'tanh':
            self.activation = tanh
            self.activation_prime = tanh_prime

        self.layers = layers

        # Set weights
        self.weights = []
        # layers = [2,2,1]
        # range of weight values (-1,1)
        # input and hidden layers - random((2+1, 2+1)) : 3 x 3
        for i in range(1, len(layers) - 1):
            r = 2*np.random.random((layers[i-1] + 1, layers[i] + 1)) -1
            self.weights.append(r)
        # output layer - random((2+1, 1)) : 3 x 1
        r = 2*np.random.random( (layers[i] + 1, layers[i+1])) - 1
        self.weights.append(r)

    def fit(self, X, y, learning_rate=0.2, epochs=100000):
        # Add column of ones to X
        # This is to add the bias unit to the input layer
        ones = np.atleast_2d(np.ones(X.shape[0]))
        X = np.concatenate((ones.T, X), axis=1)

        for k in range(epochs):
            i = np.random.randint(X.shape[0])
            a = [X[i]]

            for l in range(len(self.weights)):
                    dot_value = np.dot(a[l], self.weights[l])
                    activation = self.activation(dot_value)
                    a.append(activation)
            # output layer
            error = y[i] - a[-1]
            deltas = [error * self.activation_prime(a[-1])]

            # we need to begin at the second to last layer
            # (a layer before the output layer)
            for l in range(len(a) - 2, 0, -1):
                deltas.append(deltas[-1].dot(self.weights[l].T)*self.activation_prime(a[l]))

            # reverse
            # [level3(output)->level2(hidden)]  => [level2(hidden)->level3(output)]
            deltas.reverse()

            # backpropagation
            # 1. Multiply its output delta and input activation
            #    to get the gradient of the weight.
            # 2. Subtract a ratio (percentage) of the gradient from the weight.
            for i in range(len(self.weights)):
                layer = np.atleast_2d(a[i])
                delta = np.atleast_2d(deltas[i])
                self.weights[i] += learning_rate * layer.T.dot(delta)

            if k % 10000 == 0: print 'epochs:', k

    def predict(self, x):
        a = np.concatenate((np.ones(1).T, np.array(x)), axis=0)
        print a
        for l in range(0, len(self.weights)):
            a = self.activation(np.dot(a, self.weights[l]))
        return a.item()


    def runexperiment(self):
        util = Util()
        util.runtest()
        userlist = util.getusers()
        # userlist.remove(1)
        print userlist
        # Training Code goes here
        for user in userlist:

            writepath = "data/result/"+ str(user) + ".txt"
            output = open(writepath, "w")

            filepath1 = "data/train/"+ str(user) + ".txt"
            fr = FileReader(filepath1)
            fr.populateData()

            # X = np.array([[0, 0],
            #               [0, 1],
            #               [1, 0],
            #               [1, 1]])
            # y = np.array([0, 1, 1, 0])
            # print fr.getInput()
            X = np.array(fr.getInput(), dtype=float)
            y = np.array(fr.getOutput(), dtype=float)

            self.fit(X, y)

            # Testing Code goes here
            filepath2 = "data/test/"+ str(user) + ".txt"

            fp = open(filepath2, "r")
            input = []
            for i in fp:
                j = i.split()
                # for k in j:
                #    k=float(k)
                #    print (type(k))
                input.append(j)
            fp.close()

            # print input
            X = np.array(input, dtype=float)

            for row in X:
                content = ""
                for r in row:
                    content += str(r) + " "

                content += str(self.predict(row)) + "\n"
                # print content
                output.write(content)
            output.close()

class FileReader:
    def __init__(self, filename):
        self.filename = filename
        self.input = []
        self.output = []

    def populateData(self):
        fp = open(self.filename,"r")

        for i in fp:

            i.rstrip()
            j = i.split()
            # for k in j:
            #    k=float(k)
            #    print (type(k))
            self.output.append(j[-1])
            j.pop()
            self.input.append(j)
        fp.close()

    def getInput(self):
        print self.input
        return self.input

    def getOutput(self):
        print self.output
        return self.output

if __name__ == '__main__':

    #Three Layer NN
    # nn = NeuralNetwork([16,9,1])
    # nn.runexperiment()

    n4layer = NeuralNetwork([16,7,5,1])
    n4layer.runexperiment()

