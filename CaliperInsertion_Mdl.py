from MdlUtilities import Field, FieldList
import dbUtils

		 
def get_csvCal_fields():

	MDtop = Field(2001)
	MDbot = Field(2001)
	HID   = Field(2031)
	MD    = Field(2001)
	MDtop.set_abbreviation('MDtop')
	MDbot.set_abbreviation('MDbot')
	HID.set_abbreviation('HID')
	MDtop.set_representation('top MD')
	MDbot.set_representation('bottom MD')
	HID.set_representation('Hole ID')
	csvCal_fields = FieldList()
	csvCal_fields.append( MDtop )
	csvCal_fields.append( MDbot )
	csvCal_fields.append( HID )
	csvCal_fields.append( MD )
	
	return csvCal_fields


def get_csvCaliperReport_fields():

	Desc  = Field(2055, altBg=True, altFg=True)
	mHID  = Field(2031, altBg=True, altFg=True)  #ID
	MDbot = Field(2001, altBg=True, altFg=True)
	MDtop = Field(2001, altBg=True, altFg=True)
	MDbot.set_abbreviation('MDbot')
	MDtop.set_abbreviation('MDtop')
	csvCaliperReport_fields = FieldList()
	csvCaliperReport_fields.append( Desc  )
	csvCaliperReport_fields.append( mHID  )
	csvCaliperReport_fields.append( MDtop )
	csvCaliperReport_fields.append( MDbot )

	return csvCaliperReport_fields


def make_weightedAverage( fields ):

	s = 0
	w = 0
	for i, (top, bot) in enumerate( zip(fields.MDtop, fields.MDbot) ):
		wi = bot-top
		w += wi
		s += wi*fields.HID[i*2]

	return s/w