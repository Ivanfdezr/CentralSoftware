import re
import dbUtils
import numpy as np

def xfloat( expression ):
	items = re.split('[ ]+',expression)
	return eval( '+'.join(items) )


with open('Base de Datos ICI Flex + UR Flex.csv','r') as f:
	lines = f.readlines()
	uRes = re.split(',',lines[0][:-1])
	fIDs = re.split(',',lines[1][:-1])
	fIDis=[]
	aux=[]
	for j,fID in enumerate(fIDs):
		k=j
		if fID not in aux:
			aux.append(fID)
			fIDis.append([])
			for i in range(fIDs.count(fID)):
				l=fIDs.index(fID,k)
				k=l+1
				fIDis[-1].append(l)
		
	cID = 5001
	for line in lines[2:]:
		items = re.split(',',line[:-1])
		query = """ insert into centralizers (centralizerID,productNumber) values ('{cID}','{number}') """.format(cID=cID,number=items[0])
		dbUtils.execute_query(query)
		#print(query+'\n')
		
		for fIDi in fIDis[1:]:
			fID = fIDs[fIDi[0]]
			uRe = uRes[fIDi[0]]
			aux = np.array(items)
			value = max(map(xfloat,aux[fIDi]))
			query = """ insert into centralizer_properties (centralizerID,fieldID,nativeUnitID,valueRepresentation) 
					values ('{cID}','{fID}',(select u.unitID from units u where u.representation='{uRe}'),'{value}') """.format(cID=cID,fID=fID,uRe=uRe,value=value)
			dbUtils.execute_query(query)
			#print(query+'\n')
		cID +=1
		#input('...')
		
