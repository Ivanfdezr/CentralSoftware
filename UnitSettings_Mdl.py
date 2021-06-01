import dbUtils
from MdlUtilities import Field, FieldList


def update_customizedUnits( parameters, units ):

	for parameter, unit in zip(parameters,units):
		
		parameterID = get_parameterID(parameter)
		unitID = get_unitID(unit)

		query = f"""
				update default_cu_units set unitID={unitID} 
				where parameterID={parameterID}
				"""
		dbUtils.execute_query(query)


def get_parametersAndUnits(unitSystem):

	defaultUnitTable = 'default_{system}_units'.format(system=unitSystem)

	query = """ select p.parameterName, u.representation from parameters p, units u, {defaultUnitTable} d
				where d.parameterID=p.parameterID and d.unitID=u.unitID""".format(defaultUnitTable=defaultUnitTable)
	items = dbUtils.execute_query(query)
	defaultUnitsPerParameter = {}
	for parameter, unit in items:
		defaultUnitsPerParameter[parameter] = unit

	query = """ select p.parameterName, p.quantityID from parameters p where p.isEditable=1 order by p.quantityID asc """
	parameterItems = dbUtils.execute_query(query)

	parameters = []
	units = []

	for parameter,quantityID in parameterItems:
		
		parameters.append(parameter)
		query = """ select u.representation from units u where u.quantityID={quantityID} """.format( quantityID=quantityID )
		items = dbUtils.execute_query(query)
		
		aux = []
		for item in items:
			aux.append( item[0] )

		aux.remove( defaultUnitsPerParameter[parameter] )
		aux.insert( 0, defaultUnitsPerParameter[parameter] )
		units.append(aux)
		
	return parameters, units


def get_parameterID(parameterName):

	query = ''' select p.parameterID from parameters p where p.parameterName="{parameterName}" '''.format( parameterName=parameterName )
	parameterID = dbUtils.execute_query(query)[0][0]

	return parameterID


def get_unitID(representation):

	query = ''' select u.unitID from units u where u.representation="{representation}" '''.format( representation=representation )
	unitID = dbUtils.execute_query(query)[0][0]

	return unitID