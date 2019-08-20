import os

names = os.listdir()
for name in names:
	if name[-3:] == '.ui':
		command = 'pyuic4 '+name+' -o '+name[:-3]+'.py -i 0'
		os.system( command )
		print( command )
