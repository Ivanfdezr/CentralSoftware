import sys
import numpy as np
import matplotlib.pyplot as plt

OH = 17
L = 1000
w = 12
D = 13
d = 11
I = np.pi/32*(D**4-d**4)
F = 30000
R = L*1e6
a = np.pi/80
b = np.pi/80
ab = (a+b)/2

x = np.linspace( 0, L, 100 )
ang = np.pi/2+a

Rot = [[np.cos(ang),-np.sin(ang)],[np.sin(ang),np.cos(ang)]]
Rot = np.array(Rot)


# E = 30e7
# K = np.sqrt(F/E/I)
# y1 = (L/2/R/K + w*L*np.sin(ab)/2/K/F)*( (np.cosh(K*x)-1)/np.tanh(K*L/2) + K*x - np.sinh(K*x) ) - w*np.sin(ab)/2/F*x**2

# xy1 = np.array([x,y1])
# XY1 = np.dot(Rot,xy1)

# plt.plot(XY1[0],XY1[1],'C0--')
# plt.plot(XY1[0],XY1[1]+D/2,'C0')
# plt.plot(XY1[0],XY1[1]-D/2,'C0')

aspr = L*0.02
E = 30e6
K = np.sqrt(F/E/I)
y = (L/2/R/K + w*L*np.sin(ab)/2/K/F)*( (np.cosh(K*x)-1)/np.tanh(K*L/2) + K*x - np.sinh(K*x) ) - w*np.sin(ab)/2/F*x**2


yoh = y*0
indexes = (np.abs(y)+D/2)>OH/2
y[indexes] = (OH/2-D/2)*y[indexes]/np.abs(y[indexes])

ohc = np.array([x-L/2,yoh])
ohp = np.array([x-L/2,(yoh+OH/2)*aspr])
ohm = np.array([x-L/2,(yoh-OH/2)*aspr])

OHc = np.dot(Rot,ohc)
OHp = np.dot(Rot,ohp)
OHm = np.dot(Rot,ohm)

plt.plot(OHc[0],OHc[1],'C0--')
plt.plot(OHp[0],OHp[1],'C0')
plt.plot(OHm[0],OHm[1],'C0')


xyc = np.array([x-L/2,y*aspr])
xyp = np.array([x-L/2,(y+D/2)*aspr])
xym = np.array([x-L/2,(y-D/2)*aspr])

XYc = np.dot(Rot,xyc)
XYp = np.dot(Rot,xyp)
XYm = np.dot(Rot,xym)

plt.plot(XYc[0],XYc[1],'C1--')
plt.plot(XYp[0],XYp[1],'C1')
plt.plot(XYm[0],XYm[1],'C1')


_a = np.array([XYc,XYp,XYm])
xmin = np.min(_a)
xmin += xmin*0.1
xmax = np.max(_a)
xmax += xmax*0.1

#

plt.xlim(xmin,xmax)
plt.ylim(xmin,xmax)


# E = 30e5
# K = np.sqrt(F/E/I)
# y2 = (L/2/R/K + w*L*np.sin(ab)/2/K/F)*( (np.cosh(K*x)-1)/np.tanh(K*L/2) + K*x - np.sinh(K*x) ) - w*np.sin(ab)/2/F*x**2

# xy2 = np.array([x,y2])
# XY2 = np.dot(Rot,xy2)

# plt.plot(XY2[0],XY2[1],'C2--')
# plt.plot(XY2[0],XY2[1]+D/2,'C2')
# plt.plot(XY2[0],XY2[1]-D/2,'C2')


plt.show()

