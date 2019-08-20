import dbUtils
from MdlUtilities import Field, FieldList


def make_description(prefix,OD,fields):
	
	return prefix +' of '+OD+' '+fields.IPOD.unit


def get_BowSpringCasingODList():

	query = """ select distinct valueRepresentation from centralizer_properties where fieldID=2009 
				and centralizerID in (select c.centralizerID from centralizer_properties c where c.fieldID=2049 and c.valueRepresentation='Bow Spring')
			"""
	items = dbUtils.execute_query(query)
	casingODList = []
	for item in items:
		casingODList.append(item[0])
		
	return casingODList


def get_RigidCasingODList():

	query = """ select distinct valueRepresentation from centralizer_properties where fieldID=2009
				and centralizerID in (select c.centralizerID from centralizer_properties c where c.fieldID=2049 and c.valueRepresentation='Rigid')
			"""
	items = dbUtils.execute_query(query)
	casingODList = []
	for item in items:
		casingODList.append(item[0])
		
	return casingODList


def set_CDBBowSpring_data_to_fields(OD, fields):
	
	query = """ select c.centralizerID, (select f.abbreviation from fields f where f.fieldID=c.fieldID), c.valueRepresentation from centralizer_properties c 
				where c.centralizerID in (select centralizerID from centralizer_properties where fieldID=2009 and valueRepresentation='{OD}')
				and c.centralizerID in (select centralizerID from centralizer_properties where fieldID=2049 and valueRepresentation='Bow Spring') 
			""".format(OD=OD)
	items = dbUtils.execute_query(query)
	
	fields.clear_content()
	index = ''
	
	for item in items:
		if index != item[0]:
			if index:
				data['i'] = item[0]
				data['Desc'] = make_description(data['Type'],OD,fields)
				fields.insert_data( data )
			index = item[0]
			data  = {}
		data[item[1]] = item[2]

	data['i'] = item[0]
	data['Desc'] = make_description(data['Type'],OD,fields)
	fields.insert_data( data )

	fields.OD = OD


def set_CDBRigid_data_to_fields(OD, fields):
	
	query = """ select c.centralizerID, (select f.abbreviation from fields f where f.fieldID=c.fieldID), c.valueRepresentation from centralizer_properties c 
				where c.centralizerID in (select centralizerID from centralizer_properties where fieldID=2009 and valueRepresentation='{OD}')
				and c.centralizerID in (select centralizerID from centralizer_properties where fieldID=2049 and valueRepresentation='Rigid')
			""".format(OD=OD)
	items = dbUtils.execute_query(query)
	
	fields.clear_content()
	index = ''
	
	for item in items:
		if index != item[0]:
			if index:
				data['i'] = item[0]
				data['Desc'] = make_description(data['Type'],OD,fields)
				fields.insert_data( data )
			index = item[0]
			data  = {}
		data[item[1]] = item[2]

	data['i'] = item[0]
	data['Desc'] = make_description(data['Type'],OD,fields)
	fields.insert_data( data )

	fields.OD = OD
	

def get_CDBBowSpring_fields():

	query = """ select c.fieldID, u.representation from units u right join centralizer_properties c on c.nativeUnitID=u.unitID 
				where c.centralizerID=(select distinct min(centralizerID) from centralizer_properties where fieldID=2049 and valueRepresentation='Bow Spring')
			"""
	items = dbUtils.execute_query(query)
	
	ProdNumber  = Field(2050, altBg=True, altFg=True)
	Type        = Field(2049, altBg=True, altFg=True, mandatory=True)
	Vendor      = Field(2051, altBg=True, altFg=True)
	IPOD        = Field(2009, altBg=True, altFg=True, mandatory=True)
	OPID        = Field(2010, altBg=True, altFg=True, mandatory=True)
	CentOD      = Field(2011, altBg=True, altFg=True, mandatory=True)
	CentID      = Field(2012, altBg=True, altFg=True, mandatory=True)
	Weight      = Field(2013, altBg=True, altFg=True, mandatory=True)
	Length      = Field(2014, altBg=True, altFg=True, mandatory=True)
	Bows        = Field(2029, altBg=True, altFg=True, mandatory=True)
	StartingF   = Field(2015, altBg=True, altFg=True, mandatory=True)
	RunningF    = Field(2016, altBg=True, altFg=True, mandatory=True)
	MinRestF    = Field(2017, altBg=True, altFg=True, mandatory=True)
	RestF_SO67  = Field(2018, altBg=True, altFg=True, mandatory=True)
	SO_MinRestF = Field(2019, altBg=True, altFg=True, mandatory=True)
	MinPassThru = Field(2020, altBg=True, altFg=True)
	Descript    = Field(2055)
	CentIndex   = Field(2000)

	CDB_fields = FieldList()
	CDB_fields.append( ProdNumber  )
	CDB_fields.append( Type        )
	CDB_fields.append( Vendor      )
	CDB_fields.append( IPOD        )
	CDB_fields.append( OPID        )
	CDB_fields.append( CentOD      )
	CDB_fields.append( CentID      )
	CDB_fields.append( Weight      )
	CDB_fields.append( Length      )
	CDB_fields.append( Bows        )
	CDB_fields.append( StartingF   )
	CDB_fields.append( RunningF    )
	CDB_fields.append( MinRestF    )
	CDB_fields.append( RestF_SO67  )
	CDB_fields.append( SO_MinRestF )
	CDB_fields.append( MinPassThru )
	CDB_fields.append( Descript    )
	CDB_fields.append( CentIndex   )

	units = {}
	for item in items:
		units[item[0]] = item[1]

	for field in CDB_fields[:-2]:
		if units[field.id]:
			field.headerName = field.representation + ' ['+units[field.id]+']'
			field.unit = units[field.id]
		else:
			field.headerName = field.representation
			field.unit = None
	
	return CDB_fields
	

def get_CDBRigid_fields():

	query = """ select c.fieldID, u.representation from units u right join centralizer_properties c on c.nativeUnitID=u.unitID 
				where c.centralizerID=(select distinct min(centralizerID) from centralizer_properties where fieldID=2049 and valueRepresentation='Rigid')
			"""
	items = dbUtils.execute_query(query)
	
	ProdNumber  = Field(2050, altBg=True, altFg=True)
	Type        = Field(2049, altBg=True, altFg=True, mandatory=True)
	Vendor      = Field(2051, altBg=True, altFg=True)
	IPOD        = Field(2009, altBg=True, altFg=True, mandatory=True)
	DriftOD     = Field(2011, altBg=True, altFg=True, mandatory=True)
	MinPassThru = Field(2020, altBg=True, altFg=True, mandatory=True)
	Length      = Field(2014, altBg=True, altFg=True, mandatory=True)
	Blades      = Field(2025, altBg=True, altFg=True, mandatory=True)
	BladeLength = Field(2024, altBg=True, altFg=True, mandatory=True)
	BladeHeight = Field(2023, altBg=True, altFg=True, mandatory=True)
	ArcBlade    = Field(2022, altBg=True, altFg=True, mandatory=True)
	GapLength   = Field(2021, altBg=True, altFg=True, mandatory=True)
	FF          = Field(2027, altBg=True, altFg=True, mandatory=True)
	MaxTemp     = Field(2026, altBg=True, altFg=True)
	Descript    = Field(2055)
	CentIndex   = Field(2000)

	CDB_fields = FieldList()
	CDB_fields.append( ProdNumber  )
	CDB_fields.append( Type        )
	CDB_fields.append( Vendor      )
	CDB_fields.append( IPOD        )
	CDB_fields.append( DriftOD     )
	CDB_fields.append( MinPassThru )
	CDB_fields.append( Length      )
	CDB_fields.append( Blades      )
	CDB_fields.append( BladeLength )
	CDB_fields.append( BladeHeight )
	CDB_fields.append( ArcBlade    )
	CDB_fields.append( GapLength   )
	CDB_fields.append( FF          )
	CDB_fields.append( MaxTemp     )
	CDB_fields.append( Descript    )
	CDB_fields.append( CentIndex   )

	units = {}
	for item in items:
		units[item[0]] = item[1]

	for field in CDB_fields[:-2]:
		if units[field.id]:
			field.headerName = field.representation + ' ['+units[field.id]+']'
			field.unit = units[field.id]
		else:
			field.headerName = field.representation
			field.unit = None
	
	return CDB_fields


def save_centralizer_to_DB( centralizerItems, centralizerID ):
	
	if centralizerID:
		for item in centralizerItems:

			value = item.text()
			
			if value:
				query =	"""update centralizer_properties set valueRepresentation='{value}' 
						where centralizerID={centralizerID} and fieldID={fieldID}""".format( centralizerID=centralizerID, fieldID=item.field.id, value=value)
			else:
				query = query =	"""update centralizer_properties set valueRepresentation=NULL 
						where centralizerID={centralizerID} and fieldID={fieldID}""".format( centralizerID=centralizerID, fieldID=item.field.id)

			dbUtils.execute_query(query)

	else:
		query = "select distinct max(centralizerID) from centralizer_properties"
		centralizerID = int(dbUtils.execute_query(query)[0][0])+1

		for item in centralizerItems:

			if item.field.unit:
				query = "select u.unitID from units u where u.representation='{unit}'".format(unit=item.field.unit)
				unitID = dbUtils.execute_query(query)[0][0]
			else:
				unitID = 'NULL'

			value = item.text()
			
			if value:
				query = """insert into centralizer_properties (centralizerID,fieldID,nativeUnitID,valueRepresentation) 
						values ({centralizerID},{fieldID},{unitID},'{value}')
						""".format( centralizerID=centralizerID, fieldID=item.field.id, unitID=unitID, value=value )
			else:
				query = """insert into centralizer_properties (centralizerID,fieldID,nativeUnitID) 
						values ({centralizerID},{fieldID},{unitID})
						""".format( centralizerID=centralizerID, fieldID=item.field.id, unitID=unitID )

			dbUtils.execute_query(query)
