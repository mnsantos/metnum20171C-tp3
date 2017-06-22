#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import numpy as np
import matplotlib.pyplot as plt

def graficar_lineas(actual_temps, predicted_temps, years, actual_label):
	plt.ticklabel_format(useOffset=False)	
	plt.plot(actual_temps, label=actual_label)
	plt.plot(predicted_temps, label="Aproximacion")
	# Now add the legend with some customizations.
	plt.legend(loc='upper center', shadow=True)
	plt.xticks(range(0,len(years)+1), years, rotation='vertical')	
	plt.xlabel('Fecha'.decode('utf-8'))
	plt.ylabel('Temperatura (°C)'.decode('utf-8'))

	plt.show()