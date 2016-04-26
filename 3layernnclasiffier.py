import numpy as np


divisor = 100000

def nonlin(x,deriv=False):
    if(deriv==True):
        return x*(1-x)
    return 1/(1+np.exp(-x))



def normalize(data):
    ninput = []
    for row in data:
        temp = []
        for item in row:
            temp.append(int(item) / divisor)
        ninput.append(temp)

    return ninput


class NeuralNetwork:
    def __init__(self):
        np.random.seed(1)

        # randomly initialize our weights with mean 0
        self.syn0 = 2 * np.random.random((16, 12)) - 1
        self.syn1 = 2 * np.random.random((12, 1)) - 1


    def fit(self,X,y):

        for j in range(600000):

            # Feed forward through layers 0, 1, and 2
            l0 = X
            l1 = nonlin(np.dot(l0, self.syn0))
            l2 = nonlin(np.dot(l1, self.syn1))

            # how much did we miss the target value?
            l2_error = y - l2

            if (j % 10000) == 0:
                print ("Error:" + str(np.mean(np.abs(l2_error))))

            # in what direction is the target value?
            # were we really sure? if so, don't change too much.
            l2_delta = l2_error * nonlin(l2, deriv=True)

            # how much did each l1 value contribute to the l2 error (according to the weights)?
            l1_error = l2_delta.dot(self.syn1.T)

            # in what direction is the target l1?
            # were we really sure? if so, don't change too much.
            l1_delta = l1_error * nonlin(l1, deriv=True)

            self.syn1 += l1.T.dot(l2_delta)
            self.syn0 += l0.T.dot(l1_delta)

            weights = []
            weights.append(self.syn0)
            weights.append(self.syn1)

            self.weights = weights

    def predict(self, x):
        # a = np.concatenate((np.ones(1).T, np.array(x)), axis=0)
        # print a
        x = np.array(x)
        a = nonlin(np.dot(x, self.syn0))
        a = nonlin(np.dot(a, self.syn1))

        return a.item()

    def getweigths(self):
       return self.weights


class FileReader:



    def populate(self, filepath):
        fp = open(filepath)
        input = []
        output = []

        for i in fp:
            i.rstrip()
            j = i.split()
            # for k in j:
            #     k=float(k)
            #     print (type(k))

            output.append([j[-1]])
            j.pop()
            input.append(j)

        for i in output:
            i=list(i)

        self.input = normalize(input)
        self.output = output

    def getinput(self):
        return self.input

    def getoutput(self):
        return self.output


if __name__ == "__main__":

    nn = NeuralNetwork()

    fr = FileReader()
    fr.populate("data/train/2.txt")

    X = np.array(fr.getinput(), dtype=float)
    y = np.array(fr.getoutput(), dtype=float)

    nn.fit(X,y)

    # Testing Code goes here
    filepath2 = "data/test/2.txt"  #+ str(user) + ".txt"

    fp = open(filepath2, "r")
    input = []
    for i in fp:
        j = i.split()
        # for k in j:
        #    k=float(k)
        #    print (type(k))
        input.append(j)
    fp.close()

    X = np.array(normalize(input), dtype=float)
    # print X

    for x in X:
        print nn.predict(x)






