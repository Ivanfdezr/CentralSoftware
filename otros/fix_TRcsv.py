import re, os
import dbUtils
import numpy as np
import json

grades = ['H40','J55','K55','M65','L80','N80','C90','C95','T95','P110','Q125','TAC80','TAC95','TAC110','TAC140','TRC80','TRC95','TRC95HC','TRC110']
param_a = ['OD','Weight','Thickness','ID','Drift','Cross-section']
param_b = ['Colapso','Tension','Presion interna','Presion prueba']
tabs = ['\t\t','\t\t','\t','\t\t','\t\t','\t']
DB = []

with open('Tuberias de revestimiento_all.csv','r') as f:
	lines = f.readlines()
	bfss = []
	
	for index,line in enumerate(lines[9:]):
		a,b = re.split('[A-Za-z\-]+',line)
		afs = re.findall('([0-9]+\.[0-9]+)|([0-9]+[ 0-9\/]*)',a)
		bfs = re.findall('[0-9]+',b)
		bfss.append(bfs)
		
		if index%4 == 0:
			if afs[0][1]:
				OD = afs[0][1]
				ars = afs[1:]
			else:
				ars = afs
		
			if len(ars)==6:
				ars.pop(4)
			
			A = {param_a[0]:OD}
			for par,ar in zip(param_a[1:],ars):
				A[par] = ar[0]
				
		elif index%4 == 3:
			brss = list(zip(*bfss))
			bfss = []
			
			i = 0
			for brs in brss:
				B = {}
				for par,br in zip(param_b,brs):
					B[par] = br
				
				while True:
					os.system('clear')
					for j,k in enumerate(param_a):
						print(k+tabs[j]+A[k])
					print('\n\t'+brs[0])
					print('\t'+brs[1])
					print('\t'+brs[2])
					response = input("\t{br} == {grade} ?  ".format(br=brs[3],grade=grades[i]))
					if response=='S' or response=='':
						B['Grade'] = grades[i]
						i +=1
						break
					elif response=='N':
						i +=1
						continue
					elif response in grades:
						B['Grade'] = response
						i = grades.index(response)
						i +=1
						break
					else:
						continue
						
				P = {}
				for k,v in A.items():
					P[k] = v
				for k,v in B.items():
					P[k] = v
					
				DB.append(P)
				print(DB)

with open('TR_DB.json','w') as f:				
	f.write( json.dumps(DB, sort_keys=True, indent=4) )
			
				
		
				
