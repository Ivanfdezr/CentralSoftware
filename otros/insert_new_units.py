import re
import dbUtils

with open('unidades_nuevo','r') as f:
	lines = f.readlines()
	for line in lines:
		if line=='\n':
			continue
		#
		items = re.split('\t',line)
		query = """ insert into units (representation,factorToReferenceUnit,offsetToReferenceUnit,referenceUnit) 
					value ('{a}','{b}','{c}','{d}') """.format(a=items[1],b=items[2],c=items[3],d=items[4][:-1])
		dbUtils.execute_query(query)
