import MdlUtilities as mu
#from MdlUtilities import Field, FieldList
import pickle

MD   = mu.Field(2001)
Inc  = mu.Field(2002)
Azi  = mu.Field(2003)
TVD  = mu.Field(2004, altBg=True, altFg=True)
HD   = mu.Field(2005, altBg=True, altFg=True)
NS   = mu.Field(2006, altBg=True, altFg=True)
EW   = mu.Field(2007, altBg=True, altFg=True)
DL   = mu.Field(2008, altBg=True, altFg=True)

s2DataSurvey_fields = mu.FieldList()
s2DataSurvey_fields.append( MD  )
s2DataSurvey_fields.append( Inc )
s2DataSurvey_fields.append( Azi )
s2DataSurvey_fields.append( TVD )
s2DataSurvey_fields.append( HD  )
s2DataSurvey_fields.append( NS  )
s2DataSurvey_fields.append( EW  )
s2DataSurvey_fields.append( DL  )

with open('objfiles/test.obj','wb') as File:
	P=pickle.Pickler(File)
	P.dump(s2DataSurvey_fields)



