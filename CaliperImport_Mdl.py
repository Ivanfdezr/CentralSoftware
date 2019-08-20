import re
import numpy as np
import numpy.linalg as la
import codecs
from MdlUtilities import Field, FieldList
import MdlUtilities as mdl
import dbUtils


def get_lengthUnits():

	query = 'select u.representation from units u, quantities q where u.quantityID=q.quantityID and q.quantityName="length"'
	items = dbUtils.execute_query(query)
	units = [ item[0] for item in items ]

	return units


def get_ciCaliperReport_fields():

	Desc  = Field(2055, altBg=True, altFg=True)
	mHID  = Field(2031, altBg=True, altFg=True)  #ID
	mBS   = Field(2046, altBg=True, altFg=True)  #Drift
	MDbot = Field(2001, altBg=True, altFg=True)
	MDtop = Field(2001, altBg=True, altFg=True)
	MDbot.set_abbreviation('MDbot')
	MDtop.set_abbreviation('MDtop')
	ciCaliperReport_fields = FieldList()
	ciCaliperReport_fields.append( Desc  )
	ciCaliperReport_fields.append( mBS   )
	ciCaliperReport_fields.append( mHID  )
	ciCaliperReport_fields.append( MDtop )
	ciCaliperReport_fields.append( MDbot )

	return ciCaliperReport_fields


def get_ciLASData_fields():

	MD  = Field(2001)
	BS  = Field(2030)
	CD  = Field(2030)
	MDs = Field(2001)
	BS.set_abbreviation('BS')
	MDs.set_abbreviation('selectedMD')
	CD.set_abbreviation('CD')
	ciLASData_fields = FieldList()
	ciLASData_fields.append( MD  )
	ciLASData_fields.append( BS  )
	ciLASData_fields.append( CD  )
	ciLASData_fields.append( MDs )
	
	return ciLASData_fields


def get_ciCALData_fields():

	CAL1  = Field(2031)
	CAL2  = Field(2031)
	CAL3  = Field(2031)
	CAL4  = Field(2031)
	CAL5  = Field(2031)
	CAL6  = Field(2031)
	CAL1.set_abbreviation('CAL1')
	CAL2.set_abbreviation('CAL2')
	CAL3.set_abbreviation('CAL3')
	CAL4.set_abbreviation('CAL4')
	CAL5.set_abbreviation('CAL5')
	CAL6.set_abbreviation('CAL6')
	ciCALData_fields = FieldList()
	ciCALData_fields.append( CAL1 )
	ciCALData_fields.append( CAL2 )
	ciCALData_fields.append( CAL3 )
	ciCALData_fields.append( CAL4 )
	ciCALData_fields.append( CAL5 )
	ciCALData_fields.append( CAL6 )
	
	return ciCALData_fields


class DerivativeLevelsMatrix( object ):

	def __init__( self, MD, ID ):

		self.MD = np.array( MD )
		self.ID = np.array( ID )
		self.IDmaxOrig = np.max( self.ID, axis=0 )
		self.IDminOrig = np.min( self.ID, axis=0 )
		self.IDmax = np.array(self.IDmaxOrig)

		assert( len(self.MD)==len(self.IDmax) )
	
		"""
		dID = (self.ID[1:]-self.ID[:-1])/(self.MD[1:]-self.MD[:-1])
		abs_dID = np.abs(dID)
		maxAbs_dID = np.max(abs_dID)
		derivativeLevel = np.floor(abs_dID/maxAbs_dID*99)
		derivativeLevel = derivativeLevel.reshape(1,-1)
		"""
		dID = (self.IDmax[1:]-self.IDmax[:-1])/(self.MD[1:]-self.MD[:-1])
		abs_dID = np.abs(dID)
		maxAbs_dID = np.max(abs_dID)
		derivativeLevel = np.floor(  np.log(abs_dID+1)/np.log(maxAbs_dID+1)*99   )
		derivativeLevel = derivativeLevel.reshape(1,-1)

		levels = np.arange(101)
		levels = levels.reshape(-1,1)

		self.indexKeepingMatrix = derivativeLevel>=levels


	def get_leveredID( self, thresholdLevel ):

		indexesKeepingRow = list(self.indexKeepingMatrix[thresholdLevel])
		indexesKeepingRowL = [True] + indexesKeepingRow
		indexesKeepingRowR = indexesKeepingRow + [True]
		indexesKeepingRow = np.logical_or( indexesKeepingRowL, indexesKeepingRowR )

		avgIndexes = []
		for i,index in enumerate(indexesKeepingRow):
			if index:
				#self.ID[avgIndexes] = np.mean(self.ID[avgIndexes])
				for arm in range(len(self.ID)):
					self.ID[arm][avgIndexes] = mdl.make_cleanAverage(self.ID[arm][avgIndexes])
				self.IDmax[avgIndexes] = mdl.make_cleanAverage(self.IDmax[avgIndexes])
				avgIndexes = []
			else:
				avgIndexes.append(i)

		return list(self.ID), self.IDmax, self.IDmaxOrig, self.IDminOrig


def reduce_IDandMD( ID, MD ):

	ID = np.array(ID)
	MD = np.array(MD)

	boolIDvariance = list(ID[1:]!=ID[:-1])
	boolIDvariance_L = boolIDvariance + [True]
	boolIDvariance_R = [True] + boolIDvariance

	indexesKeepingRow = np.logical_or( boolIDvariance_L, boolIDvariance_R )

	ID = ID[indexesKeepingRow]
	MD = MD[indexesKeepingRow]

	return ID, MD


	