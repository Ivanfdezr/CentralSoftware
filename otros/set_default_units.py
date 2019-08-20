import re
import dbUtils

query = """ select * from parameters """
parameter_items = dbUtils.execute_query(query)

for pID,pNa,qID,e in parameter_items:
	query = """ select u.unitID, u.representation from units u where u.quantityID='{qID}' """.format(qID=qID)
	unit_items = dbUtils.execute_query(query)
	print('\n'+pNa+' :\n')
	for j,uRe in unit_items:
		print(j,uRe)
	uID = input('UnitID? ')
	query = """ insert into default_si_units (parameterID,unitID) values ('{pID}','{uID}') """.format(pID=pID,uID=uID)
	dbUtils.execute_query(query)
	print('\n')
