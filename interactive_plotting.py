from bokeh.plotting import figure, output_file,show
#from bokeh.io import output_file, show
from bokeh.layouts import widgetbox
from bokeh.models.widgets import Select

import numpy as np
import csv
import os



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

def all_parametres():
	problem = {
    	'num_vars'  : 0,
    	'names'     : [],
	}
	file="parametres_Info.txt"
	RAW= csv.reader(open(file, "r"), delimiter='\t')
	pass1=1
	for line in RAW:
		if pass1==1: #It don't save the first line
			pass1=0
			continue
		problem['num_vars'] += 1 
		problem['names'].append(line[0])
	return problem

def plot_comparation():
	for i in range(K):											#Parametres loop
		for j in range(2,tr,2):										#Trajectories loop
			po = int((j/2)-1)
			mu = np.loadtxt(names_mu[po])						#Import mu data
			si = np.loadtxt(names_si[po])						#Import sigma data
			if tr == 2:											#Plot for each function
				a[i].plot(j, mu[1,i], "^r", label = 'mu')
				a[i].plot(j, si[1,i], "ob", label = 'sigma')
			else :
				a[i].plot(j, mu[1,i], "^r")
				a[i].plot(j, si[1,i], "ob")

p_output=['C_do','C_cbod','C_p','C_NH4','C_NO3','C_on','C_ip','C_op','C_chl']

problem = all_parametres()


name_folder = input("name folder ?: ")
os.chdir("./"+name_folder)

names_mu, names_si, tr = all_names()

K = problem['num_vars']         #Number of parameters
P = len(p_output)               #Number of output


po = 0
mu = np.loadtxt(names_mu[po])						#Import mu data
si = np.loadtxt(names_si[po])

# Plotting
output_file("select.html")

p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')

for i in range(K):
	p.circle([2], [mu[0,i]], legend="Mu", line_width=2)
	p.circle([2], [si[0,i]], legend="Sigma", line_width=2)

s_functions = Select(title="Functions:", options=p_output)
s_parametres = Select(title="Parametres:", options=problem['names'])


show(p,widgetbox(s_functions,s_parametres))

# Changes of folder
#
#take the name of the file
#name of the folder
#

#Parametres


#Save the informacion in a problem (dictionary)
