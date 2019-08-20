import json
import dbUtils

Y = {}
Y['H40'] = [40,60]
Y['J55'] = [55,75]
Y['K55'] = [55,95]
Y['M65'] = [65,85]
Y['L80'] = [80,95]
Y['N80'] = [80,100]
Y['C90'] = [90,100]
Y['C95'] = [95,105]
Y['T95'] = [95,105]
Y['P110'] = [110,125]
Y['Q125'] = [125,135]
Y['TAC80'] = [80,100]
Y['TAC95'] = [95,110]
Y['TAC110'] = [110,125]
Y['TAC140'] = [140,150]
Y['TRC80'] = [80,95]
Y['TRC95'] = [95,105]
Y['TRC95HC'] = [95,105]
Y['TRC110'] = [110,115]

with open('TR_DB.json','r') as f:
	s = f.read()
	DB = json.loads(s)

pID = 6001
for db in DB:
	grade = db['Grade']
	query = """ insert into pipes (pipeID,vendor,grade) values ('{pID}','Tenaris Tamsa','{grade}') """.format(pID=pID,grade=grade)
	dbUtils.execute_query(query)
	
	value = db['OD']
	query = """ insert into pipe_properties (pipeID,fieldID,nativeUnitID,valueRepresentation) values
				('{pID}','2030',(select u.unitID from units u where u.representation='in'),'{value}') """.format(pID=pID,value=value)
	dbUtils.execute_query(query)
	
	value = db['ID']
	query = """ insert into pipe_properties (pipeID,fieldID,nativeUnitID,valueRepresentation) values
				('{pID}','2031',(select u.unitID from units u where u.representation='in'),'{value}') """.format(pID=pID,value=value)
	dbUtils.execute_query(query)
	
	value = db['Weight']
	query = """ insert into pipe_properties (pipeID,fieldID,nativeUnitID,valueRepresentation) values
				('{pID}','2032',(select u.unitID from units u where u.representation='lb/ft'),'{value}') """.format(pID=pID,value=value)
	dbUtils.execute_query(query)
	
	value = float(Y[grade][0])*1000
	query = """ insert into pipe_properties (pipeID,fieldID,nativeUnitID,valueRepresentation) values
				('{pID}','2033',(select u.unitID from units u where u.representation='psi'),'{value}') """.format(pID=pID,value=value)
	dbUtils.execute_query(query)
	
	value = float(db['Tension'])*1000
	query = """ insert into pipe_properties (pipeID,fieldID,nativeUnitID,valueRepresentation) values
				('{pID}','2034',(select u.unitID from units u where u.representation='lbf'),'{value}') """.format(pID=pID,value=value)
	dbUtils.execute_query(query)
	
	value = float(Y[grade][1])*1000
	query = """ insert into pipe_properties (pipeID,fieldID,nativeUnitID,valueRepresentation) values
				('{pID}','2035',(select u.unitID from units u where u.representation='psi'),'{value}') """.format(pID=pID,value=value)
	dbUtils.execute_query(query)
	
	value = db['Colapso']
	query = """ insert into pipe_properties (pipeID,fieldID,nativeUnitID,valueRepresentation) values
				('{pID}','2036',(select u.unitID from units u where u.representation='psi'),'{value}') """.format(pID=pID,value=value)
	dbUtils.execute_query(query)
	
	value = db['Presion interna']
	query = """ insert into pipe_properties (pipeID,fieldID,nativeUnitID,valueRepresentation) values
				('{pID}','2037',(select u.unitID from units u where u.representation='psi'),'{value}') """.format(pID=pID,value=value)
	dbUtils.execute_query(query)
	
	value = db['Presion prueba']
	query = """ insert into pipe_properties (pipeID,fieldID,nativeUnitID,valueRepresentation) values
				('{pID}','2038',(select u.unitID from units u where u.representation='psi'),'{value}') """.format(pID=pID,value=value)
	dbUtils.execute_query(query)
	
	query = """ insert into pipe_properties (pipeID,fieldID,nativeUnitID,valueRepresentation) values
				('{pID}','2039',(select u.unitID from units u where u.representation='g/cm³'),'7.85') """.format(pID=pID)
	dbUtils.execute_query(query)
	
	query = """ insert into pipe_properties (pipeID,fieldID,nativeUnitID,valueRepresentation) values
				('{pID}','2040',(select u.unitID from units u where u.representation='psi'),'30e6') """.format(pID=pID)
	dbUtils.execute_query(query)
	
	query = """ insert into pipe_properties (pipeID,fieldID,nativeUnitID,valueRepresentation) values
				('{pID}','2041',(select u.unitID from units u where u.representation='1'),'0.3') """.format(pID=pID)
	dbUtils.execute_query(query)
	
	query = """ insert into pipe_properties (pipeID,fieldID,nativeUnitID,valueRepresentation) values
				('{pID}','2045',(select u.unitID from units u where u.representation='ft'),'40') """.format(pID=pID)
	dbUtils.execute_query(query)
	
	value = db['Drift']
	query = """ insert into pipe_properties (pipeID,fieldID,nativeUnitID,valueRepresentation) values
				('{pID}','2046',(select u.unitID from units u where u.representation='in'),'{value}') """.format(pID=pID,value=value)
	dbUtils.execute_query(query)
	
	value = db['Thickness']
	query = """ insert into pipe_properties (pipeID,fieldID,nativeUnitID,valueRepresentation) values
				('{pID}','2047',(select u.unitID from units u where u.representation='in'),'{value}') """.format(pID=pID,value=value)
	dbUtils.execute_query(query)
	
	value = db['Cross-section']
	query = """ insert into pipe_properties (pipeID,fieldID,nativeUnitID,valueRepresentation) values
				('{pID}','2048',(select u.unitID from units u where u.representation='in²'),'{value}') """.format(pID=pID,value=value)
	dbUtils.execute_query(query)
	
	pID+=1
	
	

