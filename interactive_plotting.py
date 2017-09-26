#interactive_plotting.py
#bokeh serve --show interactive_plotting.py

from bokeh.layouts import row, widgetbox
from bokeh.models import Select
from bokeh.palettes import Spectral5
from bokeh.plotting import curdoc, figure

import numpy as np
import csv
import os

def all_names():
	name_folder = input("name folder ?: ")
	os.chdir("./"+name_folder)
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


def all_parameters():
	problem = {
    	'num_vars'  : 0,
    	'names'     : [],
	}
	file="parameters_Info.txt"
	RAW= csv.reader(open(file, "r"), delimiter='\t')
	pass1=1
	for line in RAW:
		if pass1==1: #It don't save the first line
			pass1=0
			continue
		problem['num_vars'] += 1 
		problem['names'].append(line[0])
	return problem


def all_data():
	n = int(tr/2 -1)
	mu = np.array([list(np.loadtxt(names_mu[a])) for a in range(n)])
	si = np.array([list(np.loadtxt(names_si[b])) for b in range(n)])
	return mu,si


def create_figure():
	n_fun = p_output.index(s_fun.value)
	n_par = problem['names'].index(s_par.value)

	Tr = np.arange(2,tr,2)
	mus = mu[:,n_fun,n_par] 
	sis = si[:,n_fun,n_par]

	x_title = s_fun.value.title()
	y_title = s_par.value.title()


	kw = dict()
	#kw['x_range'] = sorted(set(Tr))
	kw['title'] = "%s vs %s" % ('Trajectories', 'mu/sigma')

	p = figure(plot_height=600, plot_width=800, tools='pan,box_zoom,reset', **kw)
	p.xaxis.axis_label = 'Trajectories'
	p.yaxis.axis_label = 'mu/sigma'

	sz = 9
	c = "#31AADE"
	p.line(x=Tr,y=mus,color='blue',legend='Mu')
	p.line(x=Tr,y=sis,color='red',legend='Sigma')
	p.circle(x=Tr, y=mus, color='blue', size=sz, line_color="blue",\
		alpha=0.6, hover_color='white', hover_alpha=0.5, legend='Mu')
	p.circle(x=Tr, y=sis, color='red', size=sz, line_color="red",\
		alpha=0.6, hover_color='white', hover_alpha=0.5, legend='Sigma')
	return p


def update(attr, old, new):
	layout.children[1] = create_figure()


p_output = ['C_do','C_cbod','C_p','C_NH4','C_NO3','C_on','C_ip','C_op']
problem  = all_parameters()

names_mu, names_si, tr = all_names()

K = problem['num_vars']         #Number of parameters
P = len(p_output)               #Number of output


mu,si = all_data()


#
s_fun = Select(title="Functions:", value = 'C_do', options=p_output)
s_fun.on_change('value', update)

#
s_par = Select(title="Parameteres:", value = 'k_d1', options=problem['names'])
s_par.on_change('value', update)

#
controls = widgetbox([s_fun, s_par])
layout = row(controls,create_figure())

#
curdoc().add_root(layout)
curdoc().title = 'Plotting'