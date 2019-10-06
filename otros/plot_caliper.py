import codecs
import re
import numpy as np
import matplotlib.pyplot as plt

def get_caliper( index ):
	
	file_name = 'pemex_chinchorro26_bgt-drcal-rg_984.8_0_12042018.las.txt'
	#with open(file_name,'r') as FILE:
	with codecs.open(file_name, "r",encoding='utf-8', errors='ignore') as FILE:
		lines = FILE.readlines()
	
		section_count = 0
		ready_flag = False
		rows = []
	
		for line in lines:
			if line[0]=='~':
				section_count +=1
				if section_count==4:
					ready_flag = True
					continue
			if ready_flag and line[0]!='#':
				L = np.array( re.split('[\s]+',line) )
				##
				items = np.array(list(map(float,L[L!=''])))
				##
				rows.append( items[index] )
	MD = []
	ID = []
	
	for row in rows:
		if any(row<0):
			continue
		MD.append(row[0])
		ID.append(row[1])
	
	return MD,ID

	
if __name__=='__main__':
	MD,ID = get_caliper([0,3])
	ID = np.array(ID)
	plt.plot( ID/2,MD,'b-')
	plt.plot(-ID/2,MD,'b-')
	plt.plot([-13,-13],[MD[0],MD[-1]],'r-')
	plt.plot([13,13],[MD[0],MD[-1]],'r-')
	plt.show()
	
	
	
	
