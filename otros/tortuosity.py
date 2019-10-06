import re
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import numpy as np

with open('MD_Inc_Azi.txt','r') as f:
	lines = f.readlines()

MD = []
In = []
Az = []
factor = np.pi/180

for line in lines:
	md,inc,azi = map(float,re.split('\t',line))
	MD.append(md)
	In.append(inc*factor)
	Az.append(azi*factor)

s = np.array(MD)

lE = np.sin(In)*np.sin(Az)
lN = np.sin(In)*np.cos(Az)
lV = np.cos(In)

l = np.array(list(zip(lE,lN,lV)))
h = np.array(s[1:]-s[:-1])
u = np.array(2*(h[1:]+h[:-1]))

v = 6*( (l[2:]-l[1:-1])/h[1:,None] - (l[1:-1]-l[:-2])/h[:-1,None] )
m = len(v)

M = np.zeros((m,m))
M[0,0] = u[0]+h[0]+h[0]**2/h[1]
M[0,1] = h[1]-h[0]**2/h[1]
M[-1,-2] = h[-2]-h[-1]**2/h[-2]
M[-1,-1] = u[-1]+h[-1]+h[-1]**2/h[-2]

for i in range(1,m-1):
	M[i,i-1] = h[i-1]
	M[i,i]   = u[i]
	M[i,i+1] = h[i]

M = np.matrix(M)
I = M.I
z = np.array(I*v)
z = list(z)
z.insert( 0, z[0]-h[0]*(z[1]-z[0])/h[1] )
z.append( z[-1]-h[-1]*(z[-1]-z[-2])/h[-2] )
z = np.array(z)

A = l[:-1]
B = (l[1:]-l[:-1])/h[:,None] - h[:,None]*z[1:]/6 - h[:,None]*z[:-1]/3
C = z[:-1]/2
D = (z[1:]-z[:-1])/6/h[:,None]

Y = [np.array([0,0,0])]
T = lambda i,S: A[i] + (S-s[i])*B[i] + (S-s[i])**2*C[i] + (S-s[i])**3*D[i]
Z = lambda i,S: (S-s[i])*A[i] + (S-s[i])**2/2*B[i] + (S-s[i])**3/3*C[i] + (S-s[i])**4/4*D[i]

for hi,Ai,Bi,Ci,Di in zip(h,A,B,C,D):
	Y.append( Y[-1] + hi*Ai + hi**2/2*Bi + hi**3/3*Ci + hi**4/4*Di )
	
R = []
for i,Yi in enumerate(Y[:-1]):
	Ss = np.linspace( s[i], s[i+1], np.floor(s[i+1]-s[i])/0.1 )
	dS = Ss[1]-Ss[0]
	for S in Ss:
		ts = T(i,S)
		w = np.array([ts[1],-ts[0],0])
		fw = np.sqrt(sum(w**2))
		if fw: w = w/fw

		R.append( Yi + Z(i,S) + 0.2*w*np.sin(S*0.25) )


R = np.array(R)
##

fig = plt.figure()
ax = fig.gca(projection='3d')

E,N,V = list(zip(*Y))
ax.plot(E,N,V)
E,N,V = list(zip(*R))
ax.plot(E,N,V)
ax.set_xlabel('E')
ax.set_ylabel('N')
ax.set_zlabel('V')
ax.set_zlim(max(V),min(V))
plt.show()

