import dbUtils
from MdlUtilities import Field, FieldList


def get_pipeODList():

	query = """ select distinct valueRepresentation from pipe_properties where fieldID=2030 """
	items = dbUtils.execute_query(query)
	pipeODList = []
	for item in items:
		pipeODList.append(item[0])
		
	return pipeODList
	

def make_description(prefix,OD,Grade,fields):
	
	return prefix +' of '+OD+' '+fields.OD.unit+', '+Grade


def set_TDB_data_to_fields(OD, fields):
	
	query = """ select p.pipeID, (select f.abbreviation from fields f where f.fieldID=p.fieldID), p.valueRepresentation from pipe_properties p 
				where p.pipeID in (select pipeID from pipe_properties where fieldID=2030 and valueRepresentation='{OD}') """.format(OD=OD)
	items = dbUtils.execute_query(query)
	
	fields.clear_content()
	index = ''
	
	for item in items:
		if index != item[0]:
			if index:
				data['i'] = item[0]
				data['Desc'] = make_description(data['Type'],OD,data['Grade'],fields)
				fields.insert_data( data )
			index = item[0]
			data  = {}
		data[item[1]] = item[2]

	data['i'] = item[0]
	data['Desc'] = make_description(data['Type'],OD,data['Grade'],fields)
	fields.insert_data( data )
	

def get_TDB_fields():

	query = """ select p.fieldID, u.representation from pipe_properties p left join units u on p.nativeUnitID=u.unitID 
				where p.pipeID=(select distinct min(pipeID) from pipe_properties)
			"""
	items = dbUtils.execute_query(query)
	
	units = {}
	for item in items:
		units[item[0]] = item[1]
	
	ProdNumber = Field(2050, altBg=True, altFg=True)
	Type       = Field(2049, altBg=True, altFg=True, mandatory=True)
	Vendor     = Field(2051, altBg=True, altFg=True)
	Grade      = Field(2052, altBg=True, altFg=True)
	Weight     = Field(2032, altBg=True, altFg=True, mandatory=True)
	OD         = Field(2030, altBg=True, altFg=True, mandatory=True)
	ID         = Field(2031, altBg=True, altFg=True, mandatory=True)
	Drift      = Field(2046, altBg=True, altFg=True, mandatory=True)
	Thickness  = Field(2047, altBg=True, altFg=True)
	CrossSec   = Field(2048, altBg=True, altFg=True)
	Density    = Field(2039, altBg=True, altFg=True, mandatory=True)
	E          = Field(2040, altBg=True, altFg=True, mandatory=True)
	v          = Field(2041, altBg=True, altFg=True, mandatory=True)
	#FF         = Field(2027, altBg=True, altFg=True, mandatory=True)
	Length     = Field(2045, altBg=True, altFg=True, mandatory=True)
	YieldTen   = Field(2034, altBg=True, altFg=True, mandatory=True)
	TYS        = Field(2033, altBg=True, altFg=True, mandatory=True)
	UTS        = Field(2035, altBg=True, altFg=True, mandatory=True)
	YieldTor   = Field(2070, altBg=True, altFg=True, mandatory=True)
	SYS        = Field(2069, altBg=True, altFg=True, mandatory=True)
	USS        = Field(2068, altBg=True, altFg=True, mandatory=True)
	Collapse   = Field(2036, altBg=True, altFg=True, mandatory=True)
	MaxIntP    = Field(2037, altBg=True, altFg=True, mandatory=True)
	TestP      = Field(2038, altBg=True, altFg=True)
	Upset      = Field(2053, altBg=True, altFg=True)
	Connection = Field(2054, altBg=True, altFg=True)
	TJOD       = Field(2042, altBg=True, altFg=True)
	TJID       = Field(2043, altBg=True, altFg=True)
	TJL        = Field(2044, altBg=True, altFg=True)
	Descript   = Field(2055)
	PipeID     = Field(2000)
	
	TDB_fields = FieldList()
	TDB_fields.append( ProdNumber  )
	TDB_fields.append( Type        )
	TDB_fields.append( Vendor      )
	TDB_fields.append( Grade       )
	TDB_fields.append( Weight      )
	TDB_fields.append( OD          )
	TDB_fields.append( ID          )
	TDB_fields.append( Drift       )
	TDB_fields.append( Thickness   )
	TDB_fields.append( CrossSec    )
	TDB_fields.append( Density     )
	TDB_fields.append( E           )
	TDB_fields.append( v           )
	#TDB_fields.append( FF          )
	TDB_fields.append( Length      )
	TDB_fields.append( YieldTen    )
	TDB_fields.append( TYS         )
	TDB_fields.append( UTS         )
	TDB_fields.append( YieldTor    )
	TDB_fields.append( SYS         )
	TDB_fields.append( USS         )
	TDB_fields.append( Collapse    )
	TDB_fields.append( MaxIntP     )
	TDB_fields.append( TestP       )
	TDB_fields.append( Upset       )
	TDB_fields.append( Connection  )
	TDB_fields.append( TJOD        )
	TDB_fields.append( TJID        )
	TDB_fields.append( TJL         )
	TDB_fields.append( Descript    )
	TDB_fields.append( PipeID      )
	
	for field in TDB_fields[:-2]:
		if units[field.id]:
			field.headerName = field.representation + ' ['+units[field.id]+']'
			field.unit = units[field.id]
		else:
			field.headerName = field.representation
			field.unit = None
		
	return TDB_fields
	

def save_pipe_to_DB( pipeItems, pipeID ):
	
	if pipeID:
		for item in pipeItems:

			value = item.text()
			
			if value:
				query =	"""update pipe_properties set valueRepresentation='{value}' 
						where pipeID={pipeID} and fieldID={fieldID}""".format( pipeID=pipeID, fieldID=item.field.id, value=value)
			else:
				query = query =	"""update pipe_properties set valueRepresentation=NULL 
						where pipeID={pipeID} and fieldID={fieldID}""".format( pipeID=pipeID, fieldID=item.field.id)

			dbUtils.execute_query(query)

	else:
		query = "select distinct max(pipeID) from pipe_properties"
		pipeID = int(dbUtils.execute_query(query)[0][0])+1

		for item in pipeItems:

			if item.field.unit:
				query = "select u.unitID from units u where u.representation='{unit}'".format(unit=item.field.unit)
				unitID = dbUtils.execute_query(query)[0][0]
			else:
				unitID = 'NULL'

			value = item.text()
			
			if value:
				query = """insert into pipe_properties (pipeID,fieldID,nativeUnitID,valueRepresentation) 
						values ({pipeID},{fieldID},{unitID},'{value}')
						""".format( pipeID=pipeID, fieldID=item.field.id, unitID=unitID, value=value )
			else:
				query = """insert into pipe_properties (pipeID,fieldID,nativeUnitID) 
						values ({pipeID},{fieldID},{unitID})
						""".format( pipeID=pipeID, fieldID=item.field.id, unitID=unitID )

			dbUtils.execute_query(query)

	
	
	
	
	
	
	
	
