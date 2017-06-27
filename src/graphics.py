#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import numpy as np
import matplotlib.pyplot as plt

def graficar_lineas(actual_temps, predicted_temps, years, actual_label, name):
	#plt.ticklabel_format(useOffset=False)	
	plt.plot(actual_temps, label=actual_label)
	plt.plot(predicted_temps, label="Aproximacion")
	# Now add the legend with some customizations.
	plt.legend(loc='upper center', shadow=True)
	plt.xticks(range(0,len(years)+1), years, rotation='90')	
	plt.xlabel('Fecha'.decode('utf-8'))
	plt.ylabel('Temperatura (°C)'.decode('utf-8'))

	plt.savefig(name)
	plt.show()

def graficar(xs, ys, xlabel, ylabel, name):
	plt.ticklabel_format(useOffset=False)	
	plt.scatter(xs,ys)
	# Now add the legend with some customizations.
	#plt.xticks(range(0,len(years)+1), years, rotation='vertical')	
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)

	plt.savefig(name)
	#plt.savefig("imagen")

