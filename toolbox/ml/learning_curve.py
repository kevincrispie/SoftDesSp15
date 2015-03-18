""" Exploring learning curves for classification of handwritten digits """

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import *
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression

data = load_digits()
print data.DESCR
num_trials = 100
train_percentages = range(5,95,5)
test_accuracies = np.zeros(len(train_percentages))

for i in range(len(train_percentages)):
	scores = []
	for j in range(num_trials):
		X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, train_size = train_percentages[i]/100.0)
		model = LogisticRegression(C = 0.00000000001)
		model.fit(X_train, y_train)

		scores.append(model.score(X_test,y_test))
	average = np.mean(scores)
	test_accuracies[i] = average

fig = plt.figure()
plt.plot(train_percentages, test_accuracies)
plt.xlabel('Percentage of Data Used for Training')
plt.ylabel('Accuracy on Test Set')
plt.show()
