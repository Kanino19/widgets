from bokeh.io import output_file, show
from bokeh.layouts import widgetbox
from bokeh.models.widgets import Button, RadioButtonGroup, Select, Slider


import numpy as np



def all_names():
	all_file = os.listdir()
	name_mu = 'SALib_mu_'
	name_si = 'SALib_sigma_'
	#Trajectories number
		#array of bolean: 
			#the position where "name_mu" is in each file of "all_file"
	position_mu = [name_mu in file for file in all_file]
	position_si = [name_si in file for file in all_file]
		#sum of all of True=1 and False=0
	tr = (sum(position_mu)+1)*2
	
	#all of name for mu and sigma
		#extract just the mu of sigma file of the "all_file"
	names_mu = list(np.extract(position_mu,all_file))
	names_si = list(np.extract(position_si,all_file))
	return names_mu, names_si, tr