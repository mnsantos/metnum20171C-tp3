import numpy as np
from sklearn.metrics import mean_squared_error

def cml(filas, b):
	A = np.vstack(filas)
	coeficients = np.linalg.lstsq(A, b)[0]
	return coeficients.tolist()

def mse(featuresList, coeficients, actualValues):
	predictions = [ np.dot(features, coeficients) for features in featuresList ]
	return mean_squared_error(actualValues, predictions)