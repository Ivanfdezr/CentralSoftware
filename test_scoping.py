"""
a=3
def foo(x):
	return a+x

a = 2
y = foo(5)

print(y)
"""

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