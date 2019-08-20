import re
import dbUtils

with open('Base de Datos ICI Thru.csv','r') as f:
	lines = f.readlines()
	uRes = re.split(',',lines[0][:-1])
	fIDs = re.split(',',lines[1][:-1])
	cID = 4001
	for line in lines[2:]:
		items = re.split(',',line[:-1])
		query = """ insert into centralizers (centralizerID,productNumber) values ('{cID}','{number}') """.format(cID=cID,number=items[0])
		dbUtils.execute_query(query)
		
		for fID, uRe, item in zip(fIDs[1:],uRes[1:],items[1:]): 
			query = """ insert into centralizer_properties (centralizerID,fieldID,nativeUnitID,valueRepresentation) 
					values ('{cID}','{fID}',(select u.unitID from units u where u.representation='{uRe}'),'{value}') """.format(cID=cID,fID=fID,uRe=uRe,value=item)
			dbUtils.execute_query(query)
		cID +=1
