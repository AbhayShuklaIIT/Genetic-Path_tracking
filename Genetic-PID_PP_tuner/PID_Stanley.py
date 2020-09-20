import numpy as np
import pandas as pd
from math import *
import matplotlib.pyplot as plt
import time

def dist(a,b,c,d):
	return(  (a-c)**2 + (b-d)**2  )**0.5

def close_event():
    plt.close() #timer calls this function after 3 seconds and closes the window 


def fitness(individual):
	kp , ki , kd , ks = individual
	ref_v = 5
	Lf = 1.9
	x0 = 0
	y0 = 0
	psi0 = 0
	v0 = 0
	cte_sum = 0
	epsi_sum = 0
	a0 = 0
	delta0 = 0
	pre_error = 0
	cum_error = 0

	n = 30
	dt = 0.05

	x = []
	y = []
	psi = []
	v = []
	a = []
	delta = []

	df1 = pd.read_csv('xnp.csv', index_col=0)
	df2 = pd.read_csv('ynp.csv', index_col=0)
	df3 = pd.read_csv('psinp.csv', index_col=0)
	x_path = df1.to_numpy()
	y_path = df2.to_numpy()
	psi_path = df3.to_numpy()

	# print(x_path)
	# print(y_path)
	# print(psi_path)
	# # x_path = []
	# y_path = []
	# psi_path = []

	# x[0] = x0
	x.append(x_path[0])
	# y[0] = y0
	y.append(y_path[0])
	# psi[0] = psi0
	psi.append(psi_path[0])
	# v[0] = v0
	v.append(v0)

	#-----------------
	# for PID
	for i in range(n-2):
		error = ref_v - v[i]
		cum_error = cum_error + error
		if cum_error > 0.5 :cum_error = 0
		diff_error = error - pre_error
		# a[i] = kp*error + ki * cum_error + kd * diff_error

		# print(diff_error)
		a.append(kp*error + ki * cum_error + kd * diff_error)
		pre_error = error
		distances = []
		for j in range(len(x_path)):
			ab = x_path[j]
			b = y_path[j]
			distances += [dist(ab,b,x[i],y[i])]
		cte_sum = cte_sum + min(distances)
		cp = distances.index(min(distances))
		epsi = abs(psi[i] - psi_path[cp]) # side of path to be determined
		#----------------cross product for find direction
		x_min = x_path[cp]
		y_min = y_path[cp]

		direc = x_min * y[i] - y_min * x[i]
		direction = 0
		if direc > 0 :
			direction = 1
		if direc < 0 :
			direction = -1
		
		# delta[i] = ks * epsi * direction;
		delta.append(ks * epsi * direction)

		epsi_sum = epsi_sum + abs(epsi)
		if a[i] > 5 :a[i] = 5
		if a[i] < -5 :a[i] = -5

		if delta[i] > 1 :delta[i] = 1
		if delta[i] < -1 :delta[i] = -1
		# print(a)1111111111111111111

		# v[i+1] = v[i] + a[i]*dt
		# psi[i+1] = psi[i] + v[i] * delta[i] * dt / Lf
		# x[i+1] = x[i] + v[i] * cos(psi[i]) * dt
		# y[i+1] = y[i] + v[i] * sin(psi[i]) * dt

		v.append(v[i] + a[i]*dt)
		psi.append( psi[i] + v[i] * delta[i] * dt / Lf)
		x.append(x[i] + v[i] * cos(psi[i]) * dt)
		y.append( y[i] + v[i] * sin(psi[i]) * dt)



		if v[i] < 1 :epsi_sum = epsi_sum + 200
		epsi_sum = epsi_sum - v[i]*10
		print("dir: "+str(direction)+" i:"+str(i)+" x : "+ str(x[i]) + " y: "+ str(y[i])+ " psi: "+ str(psi[i])+  " v: "+ str(v[i])+ " a: "+ str(a[i])+ " delta: "+ str(delta[i]))

	# for i in range(len(a)):


	# fig, (ax1, ax2) = plt.subplots(2)
	# fig.suptitle('Vertically stacked subplots')
	plt.plot(x_path, y_path , label = "1")
	plt.plot(x, y , label = "2")
	# plt.show()

	# ax2.plot(x, y)
	dista = dist(x[n-2],y[n-2],x[0],y[0])
	# print("Distance covered" + str(dista*1000))
	return epsi_sum + 100*cte_sum 

if __name__ == '__main__':
	print("code Started:")
	a = fitness([0.02,0.02,0.02,20])
	print("fitness :" + str(a))
	plt.show()

	a = fitness([1.2,1.2,1.2,25])
	print("fitness :" + str(a))
	plt.show()


	a = fitness([1.5,1.5,1.5,50])
	print("fitness :" + str(a))
	plt.show()
