import re
import dbUtils

with open('unit_conversor','r') as F:
	lines = F.readlines()
	quantity = None
	i = 3000
	for line in lines:
		items = re.split('[\s]+',line)
		if items[0]:
			quantity = ' '.join(items[1:])
		else:
			i +=1
			Representation = items[1].__repr__()[1:-1]
			FactorToReferenceUnit = items[2]
			ReferenceUnit = items[3].__repr__()[1:-1]
			
			query = """ insert into Units (UnitID, Representation, FactorToReferenceUnit, ReferenceUnit, QuantityID) 
						values ('{UnitID}', '{Representation}', '{FactorToReferenceUnit}', '{ReferenceUnit}', 
						( select q.QuantityID from Quantities q where q.QuantityName='{quantity}' ) ) """.format(UnitID=i,Representation=Representation, FactorToReferenceUnit=FactorToReferenceUnit, ReferenceUnit=ReferenceUnit, quantity=quantity)			
			dbUtils.execute_query(query)
