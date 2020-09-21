"""
a=3
def foo(x):
	return a+x

a = 2
y = foo(5)

print(y)


PL = 12

def foo(E):
	Δ = []
	aux = 0
	for join in E:
		if len(join)==1:
			Δ.append( aux+PL/2 )
			aux = PL/2
		elif len(join)==2:
			Δ.append( aux+PL/4 )
			Δ.append( PL/2 )
			aux = PL/4
		elif len(join)==3:
			Δ.append( aux+PL/4 )
			Δ.append( PL/4 )
			Δ.append( PL/4 )
			aux = PL/4
		else:
			Δ.append( aux+PL )
			aux = 0
	return Δ

configurations = {	('b', None,None): {'nest':[['A']],'label':'=\n|\nA\n|\n='},
					('r', None,None): {'nest':[['A']],'label':'=\n/\nA\n/\n='},
					('b', 'b', None): {'nest':[['A','B']],'label':'=\nA\n|\nB\n='},
					('b', 'r', None): {'nest':[['A'],['B']],'label':'=\n|\nA\n|\n=\n/\nB\n/\n='},
					('r', 'b', None): {'nest':[['A'],['B']],'label':'=\n/\nA\n/\n=\n|\nB\n|\n='},
					('r', 'r', None): {'nest':[['A'],['B']],'label':'=\n/\nA\n/\n=\n/\nB\n/\n='},
					('b', None,'b' ): {'nest':[['A'],[],['C']],'label':'=\n|\nA\n|\n=\n|\n|\n|\n=\n|\nC\n|\n='},
					('b', None,'r' ): {'nest':[['A'],[],['C']],'label':'=\n|\nA\n|\n=\n|\n|\n|\n=\n/\nC\n/\n='},
					('r', None,'b' ): {'nest':[['A'],[],['C']],'label':'=\n/\nA\n/\n=\n|\n|\n|\n=\n|\nC\n|\n='},
					('r', None,'r' ): {'nest':[['A'],[],['C']],'label':'=\n/\nA\n/\n=\n|\n|\n|\n=\n/\nC\n/\n='},
					('b', 'b', 'b' ): {'nest':[['A','B','C']],'label':'=\nA\nB\nC\n='},
					('b', 'b', 'r' ): {'nest':[['A','B'],['C']],'label':'=\nA\n|\nB\n=\n/\nC\n/\n='},
					('r', 'b', 'b' ): {'nest':[['A'],['B','C']],'label':'=\n/\nA\n/\n=\nB\n|\nC\n='},	
					('b', 'r', 'b' ): {'nest':[['A'],['B'],['C']],'label':'=\n|\nA\n|\n=\n/\nB\n/\n=\n|\nC\n|\n='},
					('b', 'r', 'r' ): {'nest':[['A'],['B'],['C']],'label':'=\n|\nA\n|\n=\n/\nB\n/\n=\n/\nC\n/\n='},
					('r', 'r', 'b' ): {'nest':[['A'],['B'],['C']],'label':'=\n/\nA\n/\n=\n/\nB\n/\n=\n|\nC\n|\n='},
					('r', 'b', 'r' ): {'nest':[['A'],['B'],['C']],'label':'=\n/\nA\n/\n=\n|\nB\n|\n=\n/\nC\n/\n='},
					('r', 'r', 'r' ): {'nest':[['A'],['B'],['C']],'label':'=\n/\nA\n/\n=\n/\nB\n/\n=\n/\nC\n/\n='}	}

for conf in configurations.values():
	E = conf['nest']
	print( E,foo(E) )



import numpy as np
import random as r

def get_sortedIndexes_of_wellboreInnerStageData(D):

	stages = D.values()
	keys = np.array(list(D.keys()))
	
	def mapfunction( stage ): 
		if stage['MDtop']==None:
			return np.inf
		else:
			return stage['MDtop']
			
	MDtops = list(map( mapfunction, stages ))
	sortedIndexes = np.argsort( MDtops )
	sortedRows = keys[sortedIndexes]

	return sortedRows


def make_D(n):
	D = {}
	for i in [0,2,4,1,3]:
		if r.random()>0.7:
			D[i] = {'MDtop':None}
		else:
			D[i] = {'MDtop':r.random()*1000//1}
	return D


for t in range(100):
	D = make_D(5)
	I = get_sortedIndexes_of_wellboreInnerStageData(D)
	print(t, D, I)

"""

import numpy as np
#from mayavi import mlab
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LightSource

## Test data: Matlab `peaks()`
x, y = np.mgrid[-3:3:50j,-3:3:50j]
z =  3*(1 - x)**2 * np.exp(-x**2 - (y + 1)**2) \
   - 10*(x/5 - x**3 - y**5)*np.exp(-x**2 - y**2) \
   - 1./3*np.exp(-(x + 1)**2 - y**2) 

## Mayavi
#surf = mlab.surf(x, y, z, colormap='RdYlBu', warp_scale='auto')
## Change the visualization parameters.
#surf.actor.property.interpolation = 'phong'
#surf.actor.property.specular = 0.1
#surf.actor.property.specular_power = 5


## Matplotlib
fig = plt.figure()
ax = fig.gca(projection='3d')

# Create light source object.
ls = LightSource(azdeg=0, altdeg=65)
# Shade data, creating an rgb array.
rgb = ls.shade(z, plt.cm.RdYlBu, vert_exag=1, blend_mode='soft')
surf = ax.plot_surface(x, y, z, linewidth=0, antialiased=False, facecolors=rgb)#

#lis = pu.LightSource(270, 45)
#rgb = lis.shade(mu.np.cos(Z/100), cmap=pu.cm.gist_earth, vert_exag=0.1, blend_mode='soft')
#self.s2TriDView_graphicsView.axes.plot_surface(X,Y,Z, linewidth=0, facecolors=rgb, antialiased=False, shade=True)

plt.show()
#mlab.show()